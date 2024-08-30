import ifcopenshell
from ifcopenshell.api import run

class IFCManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.model = ifcopenshell.file()
        self.project = None
        self.context = None
        self.body = None
        self.site = None
        self.building = None
        self.storey = None
        self.setup_ifc_model()

    def setup_ifc_model(self):
        # Create the IFC project
        self.project = run("root.create_entity", self.model, ifc_class="IfcProject", name="My Project")

        # Assign units to the project
        run("unit.assign_unit", self.model) 

        # Create a modeling geometry context
        self.context = run("context.add_context", self.model, context_type="Model")
        self.body = run("context.add_context", self.model, context_type="Model",
                        context_identifier="Body", target_view="MODEL_VIEW", parent=self.context)

        # Create a site, building, and storey
        self.site = run("root.create_entity", self.model, ifc_class="IfcSite", name="My Site")
        self.building = run("root.create_entity", self.model, ifc_class="IfcBuilding", name="Building A")
        self.storey = run("root.create_entity", self.model, ifc_class="IfcBuildingStorey", name="Ground Floor")

        # Assign hierarchy
        # run("aggregate.assign_object", self.model, relating_object=self.project, products=[self.site])
        # run("aggregate.assign_object", self.model, relating_object=self.site, products=[self.building])
        # run("aggregate.assign_object", self.model, relating_object=self.building, products=[self.storey])

    def save(self):
        # Write out to a file
        self.model.write(self.file_path)
        print(f"IFC file saved to: {self.file_path}")

class IFCElement:
    def __init__(self, ifc_manager, ifc_class, name):
        self.ifc_manager = ifc_manager
        self.element = run("root.create_entity", self.ifc_manager.model, ifc_class=ifc_class, name=name)

    def set_placement(self):
        # Set placement using the provided method
        run("geometry.edit_object_placement", self.ifc_manager.model, product=self.element)

    # NOTE: this method is overrided by the subclass i.e. ifc_Wall
    # def add_representation(self, length, height, thickness):
    #     # Add representation using the provided method
    #     representation = run("geometry.add_wall_representation", self.ifc_manager.model, context=self.ifc_manager.body,
    #                          length=length, height=height, thickness=thickness)
    #     run("geometry.assign_representation", self.ifc_manager.model, product=self.element, representation=representation)

    def assign_to_container(self, container):
        # Assign element to a container
        run("spatial.assign_container", self.ifc_manager.model, relating_structure=container, product=self.element)

    def add_property_set(self, property_sets):
        """
        Adds one or more property sets to the element.

        Args:
            property_sets (dict): A dictionary where keys are property set names,
                                  and values are dictionaries of property names and values.
        """
        for pset_name, properties in property_sets.items():
            # Create the property set
            pset = run("pset.add_pset", self.ifc_manager.model, product=self.element, name=pset_name)
            
            # Populate the property set with properties
            run("pset.edit_pset", self.ifc_manager.model, pset=pset, properties=properties)


