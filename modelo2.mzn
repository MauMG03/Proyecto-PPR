include "globals.mzn";

% ------------------------------ Parametros ------------------------------
enum ACTORES;
array[int] of int: Duracion;

int: n = card(ACTORES); 
int: m = length(Duracion);

array[1..n,1..m+1] of int: Escenas;
array[1..n,1..2] of int: Disponibilidad;
array[int,1..2] of int: Evitar;

% ------------------------------ Variables ------------------------------

array[1..m] of var 1..m: orden;
array[1..m] of var 1..m: pos;

array[1..n,1..m] of var {0,1}: ap;
array[1..n,1..n] of var int: tiempo;

var int: compartido;
var int: costos;

% ------------------------------ Restricciones ------------------------------

%Funcion auxiliar para determinar las escenas en las que participa un actor i
function array[int] of 1..m: scenes(int:i) = [j | j in 1..m where Escenas[i,j] = 1];
function var int: min_int(array[int] of int: x) = min([pos[i] | i in { x[i] | i in index_set(x) }]);
function var int: max_int(array[int] of int: x) = max([pos[i] | i in { x[i] | i in index_set(x) }]);

%No negatividad
constraint costos >= 0;
constraint compartido >= 0;


%Todas las escenas deben realizarse
constraint alldifferent(orden);

%Los arreglos de orden y posición de las escenas deben ser coherentes
constraint forall(i in 1..m)(orden[pos[i]] = i);

%La aparicion del actor i en un tiempo j se marca como 1
constraint forall(i in 1..n)(
  let {array[int] of int: sc = scenes(i)} in forall(j in min_int(sc)..max_int(sc))(
    ap[i,j] = 1
  )
);

%Calculo del costo total
constraint costos = sum(i in 1..n)(sum(j in 1..m)(Duracion[orden[j]] * ap[i,j]) * Escenas[i,m+1]);

% ------------------------ Restricciones Adicionales ---------------------------

%Simetrias
%soluciones espejo
constraint pos[1] <= (m + 1) div 2;

%Redundancia
%el tiempo en que aparece un actor aparece en el set es mayor o igual a la cantidad de escensa que tiene
constraint forall(i in 1..n)(sum(j in 1..m)(ap[i,j]) >= sum(j in 1..m)(Escenas[i,j]));

%Calcula todos los tiempos que comparten los actores con otros
constraint forall(i in 1..n, j in 1..n)(tiempo[i,j] = sum(k in 1..m where ap[i,k] + ap[j,k] = 2)(Duracion[orden[k]]));

%Disponibilidad
constraint forall(i in index_set_1of2(Disponibilidad) where Disponibilidad[i,2] > 0)(tiempo[i,i] <= Disponibilidad[i,2]);

%Evitar
%Suma de todos los tiempos que comparten una pareja de actores que quieren evitarse
constraint compartido = sum(i in 1..max(index_set_1of2(Evitar)))(tiempo[Evitar[i,1],Evitar[i,2]]);

% ------------------------------ Funcion Objetivo ------------------------------
solve minimize 80*costos + 20*compartido;
%solve minimize costos;

%output [show(Duracion[orden[2]] * ap[Disponibilidad[2,1],2])];