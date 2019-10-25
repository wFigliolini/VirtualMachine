#include "JVM.h"

kif *new_kif(expr* t, expr* f, expr* k){
	kif *result = (kif*) malloc(sizeof(kif));
	result->m.tag = KIF;
	result->t = t;
	result->f = f;
	result->k = k;
	return result;
}
kapp *new_kapp(expr *f, exprlist* args, expr* k){
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

expr* exprPop(exprlist** l){
    expr* result =  (*l)->e;
    void* temp = *l;
    (*l) = (*l)->l;
    free(temp);
    return result;
}

void valPush(exprlist*l, expr* e){
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

expr* VM(expr* s){
	expr *e = s;
	expr *k = NULL;
	void *temp = NULL;
    printf("Starting VM\n");
	while(1){
		enum tags currTag = e->tag; 
        printf("Current e is %i\n", currTag);
		if( currTag == IF ){
			jif* eif = (jif*) e;
			k = (expr*) new_kif(eif->t, eif->f, k);
			temp = eif;
			e = eif->c;
			free(temp);
			continue;
		}
		if( currTag == APP ){
			app* eapp = (app*) e;
			k = (expr*) new_kapp(eapp->f, eapp->args, k);
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
		enum tags kTag = k->tag; 
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
        valPush(kapp2->v, e);
        e = exprPop(&(kapp2->e));
        //Delta Function
		if(kapp2->e == NULL){
            //insert e into vals
            valPush(kapp2->v, e);
            prim* p = (prim*) kapp2->v->e;
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
                        e = (expr*) new_num(n);
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
                        e = (expr*) new_num(n);
                        break;
                    case MULT:
                        n = 1;
                        while(kapp2->v!=NULL){
                            numb = valPop(&(kapp2->v));
                            n*=numb->n;
                        }
                        e = (expr*) new_num(n);
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
                        e = (expr*) new_num(n);
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
                        e = (expr*) new_bool(n);
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
                        e = (expr*) new_bool(n);
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
                        e = (expr*) new_bool(n);
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
                        e = (expr*) new_bool(n);
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
                        e = (expr*) new_bool(n);
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
	}
}
