bl_info = {
    "name": "Vertex Maid",
    "author": "Misaki Ki",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "Properties > Object Properties > Vertex Group Specials", 
    "description": "A collection of tools to help with the maintenance of Vertex Groups",
    "category": "Mesh"
}
import bpy
import numpy as np
from bpy.types import Operator


class VERTEXMAID_OT_Vertex_Group_Bone_Cleanup(Operator):
    bl_idname = 'vertexmaid.vertex_group_bone_cleanup'
    bl_label = 'Remove Non-Bone Vertex Groups'
    bl_description = 'Removes Vertex Groups that do not have a matching bone in the selected armature.'
    

    def vertex_group_cleanup_menu(self, context):
        layout = self.layout
        
    @classmethod
    def poll(cls, context):
    # Checking if the first select object is an armature, and that only two objects are selected.
        number_of_selected_objects = len(context.view_layer.objects.selected)
        
        # Checking the amount of selected objects first, that way we don't iterate over a list if it isn't needed.
        if (number_of_selected_objects == 2):
                for objects in context.view_layer.objects.selected:
                    if objects.type == 'ARMATURE':
                        return True
        else: 
            return False
        
    def execute(self, context):
        # There's a a tiny bit of overhead from generating an unused list, but I figure this is more future-proof if I wish to extend this operation. 
        armature_object = [context.view_layer.objects.selected[i] for i, objects in enumerate(context.view_layer.objects.selected) if objects.type == 'ARMATURE']
        mesh_object = context.view_layer.objects.active
        
        
        # Checking to see if each vertex group is contained in the armature. If it is not, then we'll remove 
        # that vertex group.
        for group_index in range(len(mesh_object.vertex_groups) -1, -1, -1):
            if mesh_object.vertex_groups[group_index].name not in armature_object[0].data.bones:
                mesh_object.vertex_groups.remove( mesh_object.vertex_groups[group_index])
            
        return {'FINISHED'}
    
    
    
    #WIP
class VERTEXMAID_OT_Add_Empty_Vertex_Groups_From_Armature(Operator):
    bl_idname = 'vertexmaid.add_empty_vertex_groups_from_armature'
    bl_label = 'Add Empty Vertex Groups From Armature'
    bl_description = 'Adds Vertex Groups contained in an armature'
    

    def vertex_group_cleanup_menu(self, context):
        layout = self.layout
        
    @classmethod
    def poll(cls, context):
    # Checking if the first select object is an armature, and that only two objects are selected.
        number_of_selected_objects = len(context.view_layer.objects.selected)
        
        # Checking the amount of selected objects first, that way we don't iterate over a list if it isn't needed.
        if (number_of_selected_objects == 2):
                for objects in context.view_layer.objects.selected:
                    if objects.type == 'ARMATURE':
                        return True
        else: 
            return False
        
    def execute(self, context):
        # There's a a tiny bit of overhead from generating an unused list, but I figure this is more future-proof if I wish to extend this operation. 
        armature_object = [context.view_layer.objects.selected[i] for i, objects in enumerate(context.view_layer.objects.selected) if objects.type == 'ARMATURE']
        mesh_object = context.view_layer.objects.active
        
        
      
        # Checking to see if the bones names are contained in the vertex groups. Adding them if not.
        group_list = []
        for group_index in range(len(mesh_object.vertex_groups)):
            group_list.append(mesh_object.vertex_groups[group_index].name)
                     
        for bone_index in range(len(armature_object[0].data.bones)):
            if armature_object[0].data.bones[bone_index].name not in group_list:
                mesh_object.vertex_groups.new(name=armature_object[0].data.bones[bone_index].name)
            
        return {'FINISHED'}
    
    
    

class VERTEXMAID_OT_Remove_Empty_Vertex_Groups(Operator):
    bl_idname = 'vertexmaid.remove_empty_vertex_groups'
    bl_label = 'Remove Empty Vertex Groups'
    bl_description = 'Removes Vertex Groups that do not contain any weights'
    
    def execute(self, context):
        mesh_object = context.view_layer.objects.active
        mesh_verticies = mesh_object.data.vertices
        
        # Searching the list in reverse (so python doesn't get jumbled up).
        for vertex_group_index in range(len(mesh_object.vertex_groups) -1, -1, -1):
            if not any(vertex_group_index in [g.group for g in v.groups if g.weight > 0.0] for v in mesh_verticies):
                 mesh_object.vertex_groups.remove(mesh_object.vertex_groups[vertex_group_index])
        return {'FINISHED'}
    
class VERTEXMAID_OT_Find_Selected_Vertex_In_Shape_Keys(Operator):
    bl_idname = 'vertexmaid.find_selected_vertex_in_shape_keys'
    bl_label = 'Find Selected Vertex in Shape Keys'
    bl_description = 'Lists Shape Keys that contain the selected verticies'
    
    @classmethod
    def poll(cls, context):
        # Check if in Edit Mode
        if bpy.context.object.mode == 'EDIT' and bpy.context.object.type == 'MESH':
            return True
        
        else:
            return False 
        
    def execute(self, context):
        mesh_verticies = mesh_object.data.verticies
        # WIP /     To be Finished
        
class VERTEXMAID_OT_Select_Seam_Edges(Operator):

    me = bpy.context.object.data

    array = np.zeros(len(me.polygons), dtype=bool)
    me.polygons.foreach_set('select', array)
    array = np.zeros(len(me.vertices), dtype=bool)
    me.vertices.foreach_set('select', array)

    array = np.zeros(len(me.edges), dtype=bool)
    me.edges.foreach_get('use_seam', array)
    me.edges.foreach_set('select', array)
        
    
class VERTEXMAID_MT_VertexMaid(bpy.types.Menu):
    bl_idname = "VERTEXMAID_MT_Vertex_Maid_Menu"
    bl_label = "Vertex Maid"
    
    def draw(self, context):
        self.layout.operator('vertexmaid.vertex_group_bone_cleanup', icon = 'TRASH')
        self.layout.operator('vertexmaid.remove_empty_vertex_groups')
        self.layout.operator('vertexmaid.find_selected_vertex_in_shape_keys')
        self.layout.operator('vertexmaid.add_empty_vertex_groups_from_armature')
        
    
def add_to_menu(self, context):    
    self.layout.menu(VERTEXMAID_MT_VertexMaid.bl_idname, icon = 'HEART')
    
vg_menu_classes =   (VERTEXMAID_MT_VertexMaid, 
                     VERTEXMAID_OT_Vertex_Group_Bone_Cleanup,
                     VERTEXMAID_OT_Remove_Empty_Vertex_Groups, 
                     VERTEXMAID_OT_Find_Selected_Vertex_In_Shape_Keys,
                     VERTEXMAID_OT_Add_Empty_Vertex_Groups_From_Armature)

def register():
    from bpy.utils import register_class
    for cls in vg_menu_classes:
        register_class(cls)
    bpy.types.MESH_MT_vertex_group_context_menu.append(add_to_menu)


def unregister():
    from bpy.utils import unregister_class
    for cls in vg_menu_classes:
        unregister_class(cls)
    bpy.types.MESH_MT_vertex_group_context_menu.remove(add_to_menu)


if __name__ == "__main__":
    register()
