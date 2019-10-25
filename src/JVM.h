#pragma once
#include<stdio.h>
#include<stdlib.h>
enum tags { NUM, BOOL, PRIM, IF, APP, KIF, KAPP };
enum prims { ADD, SUB, MULT, DIV, LT, LTE, EQ, GTE, GT };
typedef struct expr{
	 enum tags tag; } expr;
typedef struct exprlist{
	 expr *e;
	 struct exprlist* l; } exprlist;
typedef struct jif{
	 expr m;
	 expr *c, *t, *f; } jif;
typedef struct app{
	 expr m;
	 expr *f;
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
	 expr* t;
	 expr* f;
	 expr* k; } kif;
typedef struct kapp{ 
	 expr m;
	 exprlist* v;
	 exprlist* e;
	 expr* k; } kapp;

