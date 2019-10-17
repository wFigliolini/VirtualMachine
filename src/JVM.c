#include "JVM.h"

kif *new_kif(void* t, void* f, void* k){
	kif *result = (kif*) malloc(sizeof(kif));
	result->m.tag = KIF;
	result->t = t;
	result->f = f;
	result->k = k;
	return result;
}
kapp *new_kapp(void *f, exprlist* args, void* k){
	kapp *result = (kapp*) malloc(sizeof(kif));
	result->m.tag = KAPP;
	result->v = (exprlist*) malloc(sizeof(exprlist));
	result->v->e = f; 
	result->v->l = NULL; 
	result->e = args;
	result->k = k;
	return result;
}

num* valPop(exprlist** l){
    num* result = (num*) (*l)->e;
    void* temp = *l;
    (*l) = (*l)->l;
    free(temp);
    return result;
}
void valPush(exprlist*l, void* e){
    while(l->l!=NULL){
        l = l->l;
    }
    exprlist* newnode = (exprlist*) malloc(sizeof(exprlist));
    newnode->e = e;
    newnode->l = NULL;
}

num* new_num(int n){
    num* result = (num*) malloc(sizeof(num));
    result->m.tag=NUM;
    result->n = n;
    return result;
}
bool* new_bool(int n){
    bool* result = (bool*) malloc(sizeof(bool));
    result->m.tag=BOOL;
    result->n = n;
    return result;
}

void* VM(void* s){
	void *e = s;
	void *k = NULL;
	void *temp = NULL;
    printf("Starting VM\n");
	while(1){
		app* gt = (app*) e;
		enum tags currTag = gt->m.tag; 
        printf("Current e is %i\n", currTag);
		if( currTag == IF ){
			jif* eif = (jif*) e;
			k = new_kif(eif->t, eif->f, k);
			temp = eif;
			e = eif->c;
			free(temp);
			continue;
		}
		if( currTag == APP ){
			app* eapp = (app*) e;
			k = new_kapp(eapp->f, eapp->args, k);
			temp = eapp;
			free(temp);
			kapp* kapp1 = (kapp*) k;
			e = kapp1->e->e;
			temp = kapp1->e;
			kapp1->e = kapp1->e->l;
			free(temp);
			continue;
		}
		if( k == NULL ){
			return e;
		}
		kapp* gkt = (kapp*) k; 
		enum tags kTag = gkt->m.tag; 
        printf("Current k is %i\n", kTag);
		if( kTag == KIF ){
			bool* eb = (bool*) e;
			kif* kif1 = (kif*) k;
				free(eb);
			if(eb->n != 0){
				e = kif1->t;
				temp = kif1;
				k = kif1->k;
				free(temp);
				continue;
			}
			else{
				e = kif1->f;
				temp = k;
				k = kif1->k;
				free(temp);
				continue;
			}
		}
		kapp* kapp2 = (kapp*) k;
        //Delta Function
		if(kapp2->e == NULL){
            //insert e into vals
            valPush(kapp2->v, e);
            prim* p = kapp2->v->e;
            temp = kapp2->v;
            kapp2->v = kapp2->v->l;
            free(temp);
            if(p->m.tag == PRIM){
                int n;
                num* numb;
                switch(p->p){
                    case ADD:
                        n = 0;
                        while(kapp2->v!=NULL){
                            numb = valPop(&(kapp2->v));
                            n+=numb->n;
                        }
                        e = new_num(n);
                        break;
                    case SUB:
                        n = 0;
                        numb = valPop(&(kapp2->v));
                        if(kapp2->v == NULL){
                            n -= numb->n;
                        }
                        else{
                            n = numb->n;
                            while(kapp2->v!=NULL){
                                numb = valPop(&(kapp2->v));
                                n-=numb->n;
                            }
                        }
                        e = new_num(n);
                        break;
                    case MULT:
                        n = 1;
                        while(kapp2->v!=NULL){
                            numb = valPop(&(kapp2->v));
                            n*=numb->n;
                        }
                        e = new_num(n);
                        break;
                    case DIV:
                        n = 1;
                        numb = valPop(&(kapp2->v));
                        if(kapp2->v == NULL){
                            n /= numb->n;
                        }
                        else{
                            n = numb->n;
                            while(kapp2->v!=NULL){
                                numb = valPop(&(kapp2->v));
                                n /=numb->n;
                            }
                        }
                        e = new_num(n);
                        break;
                    case LT:
                        n = 0;
                        numb = valPop(&(kapp2->v));
                        if(kapp2->v == NULL){
                            n = n < numb->n;
                        }
                        else{
                            n = numb->n;
                            numb = valPop(&(kapp2->v));
                            n = n <numb->n;
                        }
                        e = new_bool(n);
                        break;
                    case LTE:
                        n = 0;
                        numb = valPop(&(kapp2->v));
                        if(kapp2->v == NULL){
                            n = n <= numb->n;
                        }
                        else{
                            n = numb->n;
                            numb = valPop(&(kapp2->v));
                            n = n <= numb->n;
                        }
                        e = new_bool(n);
                        break;
                    case EQ:
                        n = 0;
                        numb = valPop(&(kapp2->v));
                        if(kapp2->v == NULL){
                            n = n == numb->n;
                        }
                        else{
                            n = numb->n;
                            numb = valPop(&(kapp2->v));
                            n = n == numb->n;
                        }
                        e = new_bool(n);
                        break;
                    case GTE:
                        n = 0;
                        numb = valPop(&(kapp2->v));
                        if(kapp2->v == NULL){
                            n = n >= numb->n;
                        }
                        else{
                            n = numb->n;
                            numb = valPop(&(kapp2->v));
                            n = n >= numb->n;
                        }
                        e = new_bool(n);
                        break;
                    case GT:
                        n = 0;
                        numb = valPop(&(kapp2->v));
                        if(kapp2->v == NULL){
                            n = n > numb->n;
                        }
                        else{
                            n = numb->n;
                            numb = valPop(&(kapp2->v));
                            n = n >numb->n;
                        }
                        e = new_bool(n);
                        break;
                }
            }
            else{
                e = kapp2->e->e;
            }
            //free kapp after completion of function
            temp = kapp2;
            k = kapp2->k;
			free(temp);
		}
		else{
			valPush(kapp2->v, e);
			e = kapp2->e->e;
			temp = kapp2->e;
			kapp2->e = kapp2->e->l;
			free(temp);
			continue;
		}
	}
}
