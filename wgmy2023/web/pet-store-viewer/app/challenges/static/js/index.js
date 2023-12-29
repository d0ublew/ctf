function filterItems() {
    var searchInput = document.getElementById("search-bar").value.toLowerCase();
    var itemRows = document.getElementsByClassName("item-row");

    for (var i = 0; i < itemRows.length; i++) {
        var itemName = itemRows[i].getAttribute("data-itemname").toLowerCase();
        var itemDescription = itemRows[i].getAttribute("data-description").toLowerCase();
        var display = "none";

        if (itemName.includes(searchInput) || itemDescription.includes(searchInput)) {
            display = "flex";
        }

        itemRows[i].style.display = display;
    }
}