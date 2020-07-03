
 # Rapport AD70 de Thibaut Rousseaux  et Gabriel Razafindratsima 


### Q1.
Il faut faire attention au nombre d'objet et de poids, car la capacité du sac peut-être excédé. Pour valeur max de la valeur d'un objet ou la taille du sac a pour effet de modifier la valeur de base de la fitness.
De plus on a noté que:

 - Si on augmente le nombre d’objet sans augmenter la capacité, on voit
   la valeur qui passe à 0 et la fitness valant 0 malgré un poids
   différent de 0.  
 - Si on augmente le nombre d’objets en augmentant la
   capacité max on voit la fitness augmenter avec une valeur !=0.  
 - Dès que le sac se craque (poids total >capacité), la fitness passe à
   0 et   donc aucune solution n’est retenue.

### Q4.
Nous n'avons pas réussi à trouver des améliorations mais plusieurs pistes sont possibles :

 - Augmenter le nombre d'itérations pour trouver un meilleur résultats.
 - peut-être améliorer les conditions et comment on test les résultats.
