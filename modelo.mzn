include "globals.mzn";

% ------------------------------ Parametros ------------------------------
int: n = card(ACTORES); 
int: m = length(Duracion);

set of string: ACTORES;
array[int] of int: Duracion;

array[1..n,1..m+1] of int: Escenas;

% ------------------------------ Variables ------------------------------

array[1..m] of var 1..n: orden;
array[1..n,1..m] of var {0,1}: ap;

% ------------------------------ Restricciones ------------------------------



constraint alldifferent(orden);


 
% ------------------------------ Funcion Objetivo ------------------------------

