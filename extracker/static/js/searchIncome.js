const textSearch = document.querySelector("#textSearch");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

textSearch.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;
    console.log(searchValue);
  
    if (searchValue.trim().length > 0) {
      tbody.innerHTML = "";
      fetch("search-income", {
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
            noResults.style.display = "block";
            tableOutput.style.display = "none";
          } else {
            noResults.style.display = "none";
            data.forEach((item) => {
              tbody.innerHTML += `
                  <tr>
                  <td>${item.amount}</td>
                  <td>${item.source}</td>
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
      tableOutput.style.display = "none";
      appTable.style.display = "block";
    }
  });
  