include "globals.mzn";

% ------------------------------ Parametros ------------------------------
enum ACTORES;
array[int] of int: Duracion;

int: n = card(ACTORES); 
int: m = length(Duracion);

array[ACTORES,1..m+1] of int: Escenas;

% ------------------------------ Variables ------------------------------

array[1..m] of var 1..m: posicion;%posicion[i]: posicion en la que se ensayara la escena i 
array[1..m] of var 1..m: escena_posicion;%escena_posicion[i]:Posicion en la que estaba inicialmente la escena.

array[ACTORES] of var 1..m: primera_escena;
array[ACTORES] of var 1..m: ultima_escena;
array[ACTORES] of var int: tiempo;

% ------------------------------ Restricciones ------------------------------

% Relacion posicion <-> escena_posicion
constraint alldifferent(posicion);
constraint alldifferent(escena_posicion);
constraint forall(escena in 1..m)(escena_posicion[posicion[escena]] = escena);

% Calcular primera_escena y ultima_escena aparicion
constraint forall(actor in ACTORES)(
  primera_escena[actor] = min([posicion[escena] | escena in 1..m where Escenas[actor, escena] = 1])
);

constraint forall(actor in ACTORES)(
  ultima_escena[actor] = max([posicion[escena] | escena in 1..m where Escenas[actor,escena] = 1])
);

constraint forall(actor in ACTORES)(
  primera_escena[actor] <= ultima_escena[actor]
);



% Tiempo de permanencia por actor
constraint forall(actor in ACTORES)(
  tiempo[actor] = sum(escena in 1..m where escena >= primera_escena[actor] /\ escena <= ultima_escena[actor]) (
    let { var int: e = escena_posicion[escena] } in Duracion[e]
  )
);



 
% ------------------------------ Funcion Objetivo ------------------------------
solve :: int_search(posicion, first_fail, indomain_min, complete)
      minimize sum(actor in ACTORES)(tiempo[actor] * Escenas[actor,m+1]);