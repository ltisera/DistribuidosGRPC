let colorCount = 1;
let sizeCount = 1;

function addColor() {
    colorCount++;
    const rows = document.querySelectorAll('.row');

    // Add a new checkbox column to each row
    rows.forEach((row, index) => {
        const cell = document.createElement('div');
        cell.className = 'cell';
        
        // If it's the first row, add a new color input
        if (index === 0) {
            cell.innerHTML = `<input type="text" placeholder="Color" id="colorInput${colorCount}">`;
        } else {
            cell.innerHTML = `<input id="color:${colorCount},talle:${index}" type="checkbox">`;
        }
        
        row.appendChild(cell);
    });
}

function addSize() {
    sizeCount++;
    
    // Create a new row for the size
    const sizeRow = document.createElement('div');
    sizeRow.className = 'row';

    // Add the size input in the first cell
    const sizeCell = document.createElement('div');
    sizeCell.className = 'cell';
    sizeCell.innerHTML = `<input type="text" placeholder="Talle" id="sizeInput${sizeCount}">`;
    sizeRow.appendChild(sizeCell);

    // Add a checkbox for each color
    for (let i = 1; i <= colorCount; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.innerHTML = `<input id="color:${i},talle:${sizeCount}" type="checkbox">`;
        sizeRow.appendChild(cell);
    }

    // Append the new size row to the matrix
    const matrix = document.getElementById('matrix');
    matrix.appendChild(sizeRow);
}

function removeColor() {
    if (colorCount > 1) {
        colorCount--;
        const rows = document.querySelectorAll('.row');

        // Remove the last color input (the last column) from each row
        rows.forEach((row, index) => {
            // Remove the second-to-last element in each row, which corresponds to the color or checkbox
            if (row.children.length > 2) {
                row.removeChild(row.children[row.children.length - 2]);
            }
        });
    }
}

function removeSize() {
    if (sizeCount > 1) {
        sizeCount--;
        const matrix = document.getElementById('matrix');
        const lastRow = matrix.children[matrix.children.length - 2]; // Get the last size row

        matrix.removeChild(lastRow); // Remove the last row before the button row
    }
}