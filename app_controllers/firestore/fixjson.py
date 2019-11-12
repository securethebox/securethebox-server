import json
# from ete3 import Tree
from treelib import Node, Tree

t = Tree()

class Flower(object):
    def __init__(self, color):
        self.color = color

def createChild(name,cn, parent_cn, path):
    t.create_node(name, cn, parent=parent_cn, data="test")
    if 'children' in path:
        for i in path['children']:
            a_name = str({"label": path['children'][i]['name']})
            a_cn = cn+'.'+path['children'][i]['cn']
            a_parent = cn
            # print(a_name)
            try:
                if 'children' in path['children'][i]:
                    createChild(a_name,a_cn,a_parent,path['children'][i])
                else:
                    # print(">>>>> no children...")
                    t.create_node(a_name, a_cn, parent=a_parent)
            except:
                print(">>>>>>>problem",a_name,a_cn,a_parent)
                break
    else:
        print('>>>>>>>> no children!')
           

def main():
    # create tree

    # open and read json file
    with open('test.json', 'r+') as f:
        data = json.load(f)
    
    t.create_node("Root", "root")
    for i in data:
        A_name = str({"label": data[i]["name"]})
        A_cn = "root"+'.'+data[i]["cn"]
        createChild(A_name,A_cn,"root",data[i])
        # t.create_node(A_name, A_cn,parent="root")
        # if 'children' in data[i]:
        #     for c in data[i]['children']:
        #         B_name = data[i]["children"][c]['name']
        #         B_cn = data[i]["children"][c]['cn']
        #         B_parent = data[i]["cn"]
        #         if 'children' in data[i]['children'][c]:
        #             t.create_node(B_name, B_cn, parent=B_parent)
        #             try:
        #                 for d in data[i]['children'][c]['children']:
        #                     C_name = data[i]['children'][c]['children'][d]['name']
        #                     C_cn = data[i]['children'][c]['children'][d]['cn']
        #                     C_parent = B_cn
        #                     if 'children' in data[i]['children'][c]['children'][d]:
        #                         t.create_node(C_name, C_cn, parent=C_parent)
        #                         try:
        #                             for x in data[i]['children'][c]['children'][d]['children']:
        #                                 D_name = data[i]['children'][c]['children'][d]['children'][x]['name']
        #                                 D_cn = data[i]['children'][c]['children'][d]['children'][x]['cn']
        #                                 D_parent = C_cn
        #                                 if 'children' in data[i]['children'][c]['children'][d]['children'][x]:
        #                                     t.create_node(D_name, D_cn, parent=D_parent)
        #                                     try:
        #                                         for y in data[i]['children'][c]['children'][d]['children'][x]['children']:
        #                                             E_name = data[i]['children'][c]['children'][d]['children'][x]['children'][y]['name']
        #                                             E_cn = data[i]['children'][c]['children'][d]['children'][x]['children'][y]['cn']
        #                                             E_parent = C_cn
        #                                             if 'children' in data[i]['children'][c]['children'][d]['children'][x]['children'][y]:
        #                                                 t.create_node(E_name, E_cn, parent=E_parent)
        #                                             else:
        #                                                 continue
        #                                     except:
        #                                         continue
        #                                 else:
        #                                     continue 
        #                         except:
        #                             continue
        #                     else:
        #                         continue
        #             except:
        #                 continue
        #         else:
        #             continue
        # else:
        #     continue
        
            

if __name__ == "__main__":
    main()
    # print(t.to_json(with_data=False))
    t.show()

    print(t.to_json(with_data=False))


    # for node in t.traverse("preorder"):
    # # Do some analysis on node
    #     print(node.render)

    # r = Rubrik()
    # r.add_parent("test")
    # r.printRubrik()
    