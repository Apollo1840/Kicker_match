"use strict";

function download() {
    const svg = document.querySelectorAll("#chart svg")[0]
    const canvas = document.getElementById("export-img");
    svg.setAttribute("width", 800);
    svg.setAttribute("height", 420);
    svg.style = "background: #ffffff";
    canvas.width = 800;
    canvas.height = 420;
    const data = new XMLSerializer().serializeToString(svg);
    const win = window.URL || window.webkitURL || window;
    const image = new Image();
    const blob = new Blob([data], {type: "image/svg+xml"});
    const url = win.createObjectURL(blob);
    image.onload = function () {
        canvas.getContext("2d").drawImage(image, 0, 0);
        win.revokeObjectURL(url);
        const uri = canvas.toDataURL("image/png").replace("image/png", "octet/stream");
        const element = document.createElement("a");
        document.body.appendChild(element);
        element.style = "display: none";
        element.href = uri;
        element.download = "stage.png";
        element.click();
        window.URL.revokeObjectURL(uri);
        document.body.removeChild(element);
    };
    image.src = url;
}

function generate() {
    const players = JSON.parse(document.getElementById("input").value.trim().replace(/'/g, "\"").replace(/\s/g, ""));

    const playersSorted = Object.keys(players).sort((a, b) => {
        if (players[a] > players[b]) {
            return -1
        } else if (players[a] === players[b]) {
            return Math.random() > Math.random() ? -1:1;
        }

        return 1;
    });
    const resultArray = playersSorted.map(name => players[name]);

    const colors = {};
    for (let index = 0; index < playersSorted.length; index++) {
        if (index < 3) {
            colors[playersSorted[index]] = "#D4AF37";
        } else if (index < 5) {
            colors[playersSorted[index]] = "#C0C0C0";
        } else if (index < 7) {
            colors[playersSorted[index]] = "#cd7f32";
        } else {
            colors[playersSorted[index]] = "#000000";
        }
    }

    const chart = c3.generate({
        bindto: "#chart",
        data: {
            rows: [
                playersSorted,
                resultArray
            ],
            type: "bar",
            colors: colors,
            labels: {
                format: (value, id) => {
                    return id + " - " + value;
                }
            }
        },
        axis: {
            rotated: true,
        },
        bar: {
            width: {
                ratio: 0.8 // this makes bar width 50% of length between ticks
            }
        }
    });
}

generate();
