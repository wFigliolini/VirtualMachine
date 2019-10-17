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

