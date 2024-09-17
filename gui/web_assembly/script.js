document.getElementById('elementType').addEventListener('change', function() {
    const selectedType = this.value;

    // Hide all specific fields initially
    document.getElementById('wallFields').style.display = 'none';
    
    // Show the form section based on the selected type
    if (selectedType === 'IfcWall') {
        document.getElementById('wallFields').style.display = 'block';
    }
});

// Event listener to toggle void fields visibility
document.getElementById('Has_Void').addEventListener('change', function() {
    const voidFields = document.getElementById('voidFields');
    if (this.checked) {
        voidFields.style.display = 'block';
    } else {
        voidFields.style.display = 'none';
    }
});

// Handler for generating or updating the IFC file
document.getElementById('generateIfc').addEventListener('click', function() {
    const wallData = {
        element_data: {
            Element_ID: 1,
            Wall_ID: document.getElementById('Wall_ID').value,
            Wall_Type: document.getElementById('Wall_Type').value,
            Height: parseFloat(document.getElementById('Height').value),
            Length: parseFloat(document.getElementById('Length').value),
            Thickness: parseFloat(document.getElementById('Thickness').value),
            Strength_Class: document.getElementById('Strength_Class').value,
        },
        geometry_data: {
            Has_Void: document.getElementById('Has_Void').checked,
            Voids: []
        }
    };

    if (wallData.geometry_data.Has_Void) {
        const void1 = {
            X: parseFloat(document.getElementById('Void1_X').value),
            Width: parseFloat(document.getElementById('Void1_Width').value),
            Height: parseFloat(document.getElementById('Void1_Height').value)
        };
        wallData.geometry_data.Voids.push(void1);
    }

    console.log('Wall Data:', wallData);
    // You can now pass this data to the backend or WebAssembly/Python processing to generate the IFC
});
