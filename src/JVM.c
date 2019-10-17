#include "JVM.h"
void* VM(void* s){
	void *e = s;
	void *k = NULL;
	void *temp = NULL;
	while(1){
		app* gt = (app*) e; 
		enum tags currTag = gt->m.tag; 
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
                        e = new_num(n)
                        break;
                    case SUB:
                        n = 0;
                        numb = valPop(&(kapp2->v));
                        if(kapp2->v == NULL){
                            n -= numb->n;
                        }
                        else{
                            
                        }
                        e = new_num(n)
                        break;
                    case MULT:
                        
                        break;
                    case DIV:
                        
                        break;
                    case LT:
                        
                        break;
                    case LTE:
                        
                        break;
                    case EQ:
                        
                        break;
                    case GTE:
                        
                        break;
                    case GT:
                        
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
