//selecting DOM elements
const textSearch = document.querySelector("#textSearch");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
// Initial setup: hiding the table output
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

// Event listener for the text search input
textSearch.addEventListener("keyup", (e) => {
  // Get the search value from the input
    const searchValue = e.target.value;
    console.log(searchValue);
  
    // Check if there's a non-empty search value
    if (searchValue.trim().length > 0) {
      tbody.innerHTML = "";
      fetch("search-expenses", {
        body: JSON.stringify({ searchText: searchValue }),
        method: "POST",
      })
        .then((res) => {
          // Log the entire response for debugging
          console.log("Response from server:", res);
          return res.json();
        })
        .then((data) => {
          console.log("data", data);
          appTable.style.display = "none";
          tableOutput.style.display = "block";
  
          if (data.length == 0) {
            // Display a message when there are no results
            noResults.style.display = "block";
            tableOutput.style.display = "none";
          } else {
            // Display the results in the table body
            noResults.style.display = "none";
            data.forEach((item) => {
              tbody.innerHTML += `
                  <tr>
                  <td>${item.amount}</td>
                  <td>${item.category}</td>
                  <td>${item.description}</td>
                  <td>${item.date}</td>
                  </tr>`;
            });
          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    } else {
      // If search value is empty, hide the search results and show the original table
      tableOutput.style.display = "none";
      appTable.style.display = "block";
    }
  });
  