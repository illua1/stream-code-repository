import bpy
import math
def inf(h):
    print();
    print(h);
    print();
    print(dir(h));
    print();
    print(type(h));
    print();
active = bpy.context.active_object;
selected = bpy.context.selected_objects;
selected.remove(active);
def floorV(v):
    v.x = math.floor(v.x)
    v.y = math.floor(v.y)
    v.z = math.floor(v.z)
    return v;
def ifConect(edg, vert, objVert, mw, cmw):
    size = 100;
    ife = 1;
    for v in edg.vertices :
        for av in objVert:
            
            if not mw == None :
                co = mw @ av.co;
            else :
                co = av.co;
                
            if not cmw == None :
                cvco = cmw @ vert[v].co;
            else :
                cvco = vert[v].co;
            if floorV(cvco.xyz*size)/size == floorV(co.xyz*size)/size :
                ife = 0;
                break
        if not ife:
            break
    if ife:
        return edgl
def EdgNormalTest(vertForEdg1, vertForEdg2) :
    size = 10;
    count = 0;
    all = [vertForEdg1[0],vertForEdg1[1],vertForEdg2[0],vertForEdg2[1]];
    for i in all:
        i -= vertForEdg2[0];
    for id in [0,1,3]:
        all[id] = all[id].normalized()
    for i in all:
        i = floorV(i*size)/size;
    
    #print("<")
    #print(all)
    
    #print("Start")
    for a in [0,1]:
        #print("New")
        for i in [1,-1]:
            print(all[a], all[1]*i)
            if all[a] == all[1]*i :
                #print("Find")
                count += 1;
    if count == 2:
        return 1;
    else :
        return 0;
if 1 :
    bpy.ops.object.select_all(action='DESELECT')
    active.select_set(1);
    bpy.ops.object.duplicate_move()
    activeCopy = bpy.context.active_object;
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    boolean = activeCopy.modifiers.new(type = 'BOOLEAN', name = 'EdgesLineFinder')
    boolean.object = selected[0];
    bpy.ops.object.modifier_apply(modifier="EdgesLineFinder")
    if 1:
        AllEdg = [];
        for edg in activeCopy.data.edges :
            n = ifConect(edg, activeCopy.data.vertices, active.data.vertices, None, None);
            if not n == None :
                AllEdg.append( n );
        end = [];
        if 1 :
            for edg in AllEdg :
                n = ifConect(edg, activeCopy.data.vertices, selected[0].data.vertices, selected[0].matrix_world, activeCopy.matrix_world);
                if not n == None :
                    end.append(n);
                    n.select = 1;
        if 1 :
            for e in end:
                for edg in active.data.edges :
                    f1 = [];
                    for i in [0,1]:
                        f1.append( activeCopy.data.vertices[e.vertices[i]].co.xyz );
                    f2 = [];
                    for i in [0,1]:
                        f2.append( active.data.vertices[edg.vertices[i]].co.xyz );
                    
                    if EdgNormalTest( f1, f2 ) :
                        e.select = 0;
                for edg in selected[0].data.edges :
                    f1 = [];
                    for i in [0,1]:
                        f1.append( activeCopy.data.vertices[e.vertices[i]].co.xyz );
                    f2 = [];
                    for i in [0,1]:
                        f2.append( selected[0].data.vertices[edg.vertices[i]].co.xyz );
                    
                    if EdgNormalTest( f1, f2 ) :
                        e.select = 0;
    if 1:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.delete(type='EDGE')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.convert(target='CURVE')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        activeCurve = bpy.context.active_object;
        activeCurve.data.bevel_depth = 0.0615;