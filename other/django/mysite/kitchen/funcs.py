import itertools

import kitchen.models

def category_is_child(c):
    cr_lst = kitchen.models.CategoryRelation.objects.all()

    for cr in cr_lst:
        if c == cr.child:
            return True

    return False

def category_get_children_list(c):
    cr_lst = kitchen.models.CategoryRelation.objects.all()

    ret = []

    for cr in cr_lst:
        if c == cr.parent:
            ret.append(cr.child)

    return ret


def category_get_children(c):
    cr_lst = kitchen.models.CategoryRelation.objects.all()

    ret = []

    for cr in cr_lst:
        if c == cr.parent:
            ret.append((
                cr.child,
                category_get_children(cr.child),
                kitchen.models.Item.objects.filter(category=cr.child)
                ))

    return ret

def category_top():
    c_lst = kitchen.models.Category.objects.all()

    ret = []

    for c in c_lst:
        if not category_is_child(c):
            ret.append(c)

    return ret

def category_top_for(c):
    if not category_is_child(c):
        return c
    
    cr_lst = kitchen.models.CategoryRelation.objects.filter(child=c)
    
    return category_top_for(cr_lst[0].parent)

def item_selector_tree2(cat_name):
    if not cat_name:
        return category_top()
    
    cat = kitchen.models.Category.objects.filter(name=cat_name)
    
    return category_get_children_list(cat[0])
     

# ir (inventory - recipe order)
# t target inventory
# b buying threshhold
def demand(ir, t=0, b=0):
    return 0 if ir > b else t - ir

def gen_transactions():
    for trans in kitchen.models.Transaction.objects.all():
        yield trans.item, trans.amount_std

def gen_recipeorder_transactions():
    for trans in kitchen.models.RecipeOrderTransaction.objects.all():
        yield trans.ingredient.item, trans.amount_std

def gen_ingredients():
    for ro in kitchen.models.RecipeOrder.objects.filter(status=kitchen.models.RecipeOrder.PLANNED):
        for ing in kitchen.models.Ingredient.objects.filter(recipe=ro.recipe):
            yield ing.item, -ing.amount_std * ro.amount


def inventory():
    grouped = itertools.groupby(gen_transactions(), lambda o: o[0])
    
    for item, gpr in grouped:
        gpr_list = list(gpr)


def recipeorder():
    grouped = itertools.groupby(gen_ingredients(), lambda o: o[0])
    
    for item, gpr in grouped:
        gpr_list = list(gpr)
        yield item, sum(a for i,a in gpr_list)

# generator of (item, ir) tuples from transactions and recipe orders
def ir_list():
    items = sorted(
            itertools.chain(gen_ingredients(), gen_transactions()),
            key = lambda o: o[0].id)
    
    grouped = itertools.groupby(items, lambda o: o[0])
    
    for item, amounts in grouped:
        amounts_list = list(amounts)
        amount = sum(amount for item,amount in amounts_list)
        yield item, amount
   

def demand_list():
    
    for item, ir in ir_list():
        
        d = demand(ir)
        
        if d > 0:
            yield item, ir, d

def myceil(x, m):
    d = x/m
    r = d % 1.0
    y = (d - r + math.ceil(r)) * m
    print("myceil x",x,"m",m,"y",y)
    return y

def test_in(G, item, d, ir_dict):
    for rec, itm, dic in G.G.in_edges(item, data=True):
        ing = dic['object']
        
        a = -d / ing.amount_std
        
        a = myceil(a, rec.lcm)
        
        yield rec, a, rec.can_make(-d / ing.amount_std, ir_dict)


