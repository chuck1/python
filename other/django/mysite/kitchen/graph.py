import subprocess
import networkx as nx

import kitchen.models



class IngGraph():
    def __init__(self):
        self.G = nx.DiGraph()
	    
	for rec in kitchen.models.Recipe.objects.all():
	    self.G.add_node(rec)
	    
	for itm in kitchen.models.Recipe.objects.all():
	    self.G.add_node(itm)
	
	for ing in kitchen.models.Ingredient.objects.all():
	    if ing.amount > 0:
	        self.G.add_edge(ing.item, ing.recipe, object=ing)
	    else:
	        self.G.add_edge(ing.recipe, ing.item, object=ing)
	
	#print(self.G.number_of_nodes())
	#print(self.G.number_of_edges())
	#print(self.G.nodes())
	#print(self.G.edges())
	#print(nx.algorithms.dag.ancestors(self.G, kitchen.models.Item.objects.get(name="pbj")))
	#print(self.G.predecessors(kitchen.models.Item.objects.get(name="pbj")))
	
    def draw(self):
        nx.write_dot(self.G, 'kitchen/static/kitchen/ing.dot')
	subprocess.call(['dot', 'kitchen/static/kitchen/ing.dot', '-Tpng', '-okitchen/static/kitchen/ing.png'])



