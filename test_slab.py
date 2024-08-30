from ifc_library.ifc_manager import IFCManager
from ifc_library.elements.ifc_slab import IFCSlab

if __name__ == "__main__":
    # Create an IFC manager instance
    ifc_manager = IFCManager("test_solid_slab.ifc")
    
    # Example slab data for a solid slab
    slab_data = {
        "element_data": {
            "Product ID": "HCS001",
            "Reinforcement ID": "RF001",
            "Count": 1,
            "Height": 200,
            "Length": 6000,
            "Width": 1200,
            "Void Count": 0,  # Ignored for solid slab
            "Void Diameter": 0.0,  # Ignored for solid slab
            "Concrete Cover": 30.0,
            "External_Web_Thickness": 50.0,
            "Concrete Strength Class": "C30/37",
            "Max Aggregate Size": 20,
            "Drawings": "http://example.com/drawing.pdf",
            "Notes": "Example notes"
        }
    }

    # Create the slab using the provided data
    slab = IFCSlab(ifc_manager, name=slab_data['element_data']['Product ID'])
    
    # Add a solid slab representation using wall representation method
    slab.add_solid_representation(
        length=slab_data['element_data']['Length'],
        width=slab_data['element_data']['Width'],
        height=slab_data['element_data']['Height']
    )
    
    # Add element data to the slab
    slab.add_element_data(slab_data['element_data'])
    
    # Assign the slab to a storey or other container
    slab.assign_to_container(ifc_manager.storey)
    
    # Save the IFC file
    ifc_manager.save()
