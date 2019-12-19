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
    exprlist* temp = *l;
    num* result = NULL;
    if(temp != NULL){
        result = (num*) temp->e;
        *l = temp->l;
    }

    return result;
}

expr* exprPop(exprlist** l){
    expr* result =  (*l)->e;
    void* temp = *l;
    (*l) = (*l)->l;
    return result;
}

void valPush(exprlist*l, expr* e){
    exprlist* temp = l;
    while(temp->l!=NULL){
        temp = temp->l;
    }
    exprlist* newnode = (exprlist*) malloc(sizeof(exprlist));
    newnode->e = e;
    newnode->l = NULL;
    temp->l = newnode;
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

void VM(expr* s, expr** r){
	expr *e = s;
	expr *k = NULL;
	void *temp = NULL;
	while(1){
		enum tags currTag = e->tag; 
		if( currTag == IF ){
			jif* eif = (jif*) e;
			k = (expr*) new_kif(eif->t, eif->f, k);
			temp = eif;
			e = eif->c;
			continue;
		}
		if( currTag == APP ){
			app* eapp = (app*) e;
			k = (expr*) new_kapp(eapp->f, eapp->args, k);
			temp = eapp;
			kapp* kapp1 = (kapp*) k;
			e = kapp1->e->e;
			temp = kapp1->e;
			kapp1->e = kapp1->e->l;
			continue;
		}
		if( k == NULL ){
			*r = e;
            return;
		}
		enum tags kTag = k->tag;
		if( kTag == KIF ){
			bool* eb = (bool*) e;
			kif* kif1 = (kif*) k;
			if(eb->n != 0){
				e = kif1->t;
				temp = kif1;
				k = kif1->k;
				continue;
			}
			else{
				e = kif1->f;
				temp = k;
				k = kif1->k;
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
		}
	}
}
