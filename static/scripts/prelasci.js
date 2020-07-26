const START = "start"
const END = "end"

const coordSystems = new Set([
    "Nebesko ekvatorski",
    "Mesno Ekvatorski",
    "Ekliptični",
    "Horizontski"
])

// Get element of the starting coordinate system
let startOptionText = "Nebesko ekvatorski"
var startCurrentOptionDiv = document.getElementById("start-system-btn")
// Get other starting options
var startOtherOptionsDiv = Object.values(document.querySelectorAll("#start-system a"))

// Get element of the ending coordinate system
let endOptionText = "Horizontski"
var endCurrentOptionDiv = document.getElementById("end-system-btn")
// Get other ending options
var endOtherOptionsDiv = Object.values(document.querySelectorAll("#end-system a"))

init()

function init() {
    // set onclick events for start
    for (let otherOption of startOtherOptionsDiv) {
        otherOption.onclick = (e) => {
            let node = e.target

            setNewOption(START, node.innerText)
        }
    }


    // set onclick events for end
    for (let otherOption of endOtherOptionsDiv) {
        otherOption.onclick = (e) => {
            let node = e.target

            setNewOption(END, node.innerText)
        }
    }
}

function setNewOption(where, newOptionText) {
    let currentOption
    let currentOthers

    let otherOption
    let otherOptions


    if (where === START) {
        startOptionText = newOptionText
        fillOtherOptions(START)
        fillOtherOptions(END)
        console.log("start")

    } else if (where === END) {
        endOptionText = newOptionText
        fillOtherOptions(END)
        fillOtherOptions(START)
        console.log("end")

    } else {
        alert("WRONG!")
        return
    }


}

// Fill drow-down menu options for start or end system
function fillOtherOptions(where) {
    let options

    if (where === START) {
        options = startOtherOptionsDiv
        startCurrentOptionDiv.innerText = startOptionText
    } else if (where === END) {
        options = endOtherOptionsDiv
        endCurrentOptionDiv.innerText = endOptionText
    } else {
        alert("ERROR!")
        return
    }

    let tmpSystems = new Set(coordSystems)
    tmpSystems.delete(startOptionText)
    tmpSystems.delete(endOptionText)
    let systemArr = [... tmpSystems]

    console.log(tmpSystems)

    for (o of options) {
        o.innerText = systemArr.pop()
    }

}