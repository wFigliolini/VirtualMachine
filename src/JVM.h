#pragma once
#include<stdio.h>
#include<stdlib.h>
enum tags { NUM, BOOL, PRIM, IF, APP, KIF, KAPP };
enum prims { ADD, SUB, MULT, DIV, LT, LTE, EQ, GTE, GT }l;
typedef struct expr{
	 enum tags tag; } expr;
typedef struct exprlist{
	 void *e;
	 struct exprlist* l; } exprlist;
typedef struct jif{
	 expr m;
	 void *c, *t, *f; } jif;
typedef struct app{
	 expr m;
	 void *f;
	 exprlist *args; } app;
typedef struct num{
	 expr m;
	 int n; } num;
typedef struct bool{
	 expr m;
	 int n; } bool;
typedef struct prim{
	 expr m;
	 enum prims p; } prim;
typedef struct kif{ 
	 expr m;
	 void* t;
	 void* f;
	 void* k; } kif;
typedef struct kapp{ 
	 expr m;
	 exprlist* v;
	 exprlist* e;
	 void* k; } kapp;
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
