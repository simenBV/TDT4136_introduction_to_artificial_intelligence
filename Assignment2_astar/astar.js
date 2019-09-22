/*
TDT4136 Introduction to Artificial Intelligence
Assignment 2 – Applying the A* Algorithm
Purpose: Gain hands-on experience with best-first search using the A* algorithm

Uses the p5 js library for visualization.

Open the browser console to get the cost of path.

1Overview:
In this assignment, you will become familiar with the A* algorithm by applying it to a classical use case
for A*, namely that of finding the shortest path in a two-dimensional grid-like world.
The assignment consists of three parts. You need to make a passable effort on the two first parts in order
to get this assignment approved.
Each of the three p
*/




// --------Global variables----------


// used python script to create array (ref zip file)
samfArray = samfArr3;

var rows = samfArray.length;
var cols = samfArray[0].length;
var grid = new Array(cols);

var width = 1000 ; 
var height = 500;
var nodeWidth ;
var nodeHeight ;


// nodes that have been visited but not expanded
var openSet = [];

// nodes that have been visited and expanded
var closedSet = [];

// current path from start to current node being evaluated
var path = [];

// ------- functions ------------------

// manhatten heuristic score
// estimates distance from node to goal;
function heuristic(node,goal,D) {
    dx = Math.abs(node.x - goal.x)
    dy = Math.abs(node.y - goal.y)
    return  D*(dx + dy)
}

// removes node from array
function removeArr(array,node) {
    for (var i=array.length-1; i>=0 ; i--) {
        if (array[i] == node) {
            array.splice(i,1);
        }
    }
}






// node class
function Node(x,y ) {
    this.x = x;
    this.y = y;
    this.f = Infinity;
    this.g = Infinity;
    this.h = 0;
    this.weight = 1 ; 
    this.cameFrom = null;
    this.wall = false;
    this.neighbors = []
    this.show = function (color) {
        fill(color);
        rect(this.x * nodeWidth, this.y *nodeHeight, nodeWidth , nodeHeight );
    }
}

function setup() {
    createCanvas(750, 750);
    console.log("INIT")

    // sets width and height of nodes to fit canvas
    nodeWidth = width / cols ; 
    nodeHeight = height / rows ; 

    for (var i = 0; i < cols; i++) {
        grid[i] = new Array(rows)   
    }

    // creates node grid
    for (var i = 0; i < cols; i++) {
        for (var j = 0; j<rows; j++) {
            grid[i][j] = new Node(i,j)
        }
    }

    // creates neighbors array
    // array = [topNeighbor, rightNeighbor, buttomNeighbor, leftNeighbor]
    for (var i = 0; i < cols; i++) {
        for (var j = 0; j<rows; j++) {
            if (j > 0) {
                grid[i][j].neighbors.push(grid[i][j-1]);
            }
            if (i <cols -1) {
                grid[i][j].neighbors.push(grid[i+1][j]);
            }
            
            if (j <rows -1) {
                grid[i][j].neighbors.push(grid[i][j+1]);
            }
            if (i > 0) {
                grid[i][j].neighbors.push(grid[i-1][j]);
            }
        }
    }

    // ###################################################//
    // ----      START INPUT SPACE             -----------//
    // ###################################################//

    // set start and goal node

    // Task 1:
    // shortest path from Rundhallen (your location) to Strossa
     //start = grid[18][27], goal = grid[31][40]
   

    // Task 2:
    // shortest path from Strossa to Selskapssiden
    // start = grid[31][40], goal = grid[5][8]

    // Task 3 and 4:
    // least cost path from Lyche to Klubben
    start = grid[32][28], goal = grid[32][6]

    // ###################################################//
    // ----      END INPUT SPACE               -----------//
    // ###################################################//
    
    // sets initial conditions
    start.g = 0 ;
    start.f = heuristic(start,goal,1)
    start.wall = false;
    goal.wall = false;
    openSet.push(start);

    
}



// draws the table using the p5.js libary
// using draw as whileloop
// while openSet is not empty
function draw() {
    if (openSet.length > 0) {

        // gets node in openSet having lowest f score
        var index = 0 ;
        for (var i = 0; i < openSet.length; i++) {
            if (openSet[i].f < openSet[index].f) {
                index = i ; 
            }
        }
        // current is now node in openSet having lowest f score
        var current = openSet[index]

        // checks if current node is the goal
        if (current === goal ) {
            console.log("DONE");
            var temp = current;
            var length = 0;
            path.push(temp);
            while (temp.cameFrom) {
                console.log(temp.weight)
                length = length + parseInt(temp.weight, 10);
                path.push(temp.cameFrom);
                temp = temp.cameFrom;
            }
            console.log("Cost: ", length);
            noLoop();
        }

        // removes current from openSet
        removeArr(openSet,current)
        
        // adds current to closedSet
        closedSet.push(current);

        // evaluates all neighbors to current
        for (var i = 0; i<current.neighbors.length; i++) {
            var neighbor = current.neighbors[i]; 

            // checks if neighbor is not in closedSet
            // and that neighbor is not wall
            if (!closedSet.includes(neighbor) && neighbor.wall != true) {
                // d is weight of edge from current to neighbor
                var d = neighbor.weight;

                // string to int
                d = parseInt(d,10)
                     
                // tentativ_gScore is distance from start 
                // to neighbor through current
                var tentativ_gScore = current.g + d  ; 

                if (tentativ_gScore < neighbor.g) {
                    // adds neighbor to path
                    neighbor.cameFrom = current ; 

                    // updates new g, h and f scores
                    neighbor.g = tentativ_gScore;
                    neighbor.h = heuristic(neighbor,goal)
                    neighbor.f = tentativ_gScore + heuristic(neighbor,goal,1);
                    if (!openSet.includes(neighbor)) {
                        openSet.push(neighbor);
                    }
                }      
            }          
        }    
    } 
    else {
        console.log("NO SOLUTION")
    }

    initGrid()
    drawingPaths()
}

// ------- functions ------------------

//creates grid and sets weights from samf array
function initGrid() {

  // createes a black background
  background(0)

  // creates the canvas grid
  for (var i = 0; i < cols; i++) {
      for (var j = 0; j<rows; j++) {

          // sets walls and draws them black
          if (samfArray[j][i] == -1 ) {
              grid[i][j].wall = true ;
              grid[i][j].show(color(0))
          }

          // sets white color to non wall and weight parameter
          else {
              grid[i][j].weight = samfArray[j][i]
              // sets light pink to nodes with weight 2
              if (samfArray[j][i] == 2 ) {
                  grid[i][j].show(color(255,182,193))
              }
              // sets pink to nodes with weight 3
              else if ((samfArray[j][i] == 3 )) {
                  grid[i][j].show(color(255,105,180))
              }
              // sets dark pink to nodes with weight 4
              else if ((samfArray[j][i] == 4 )) {
                  grid[i][j].show(color(199,21,133))
              }
              else {
              // sets white to nodes with weight 1
              grid[i][j].show(color(255))
              }
          }
      }
  }

}

// draws final path, explored and closed nodes
function drawingPaths() {
    // nodes added to the openSet are drawn yellow 
    for (var i = 0; i < openSet.length; i++) {
      openSet[i].show(color(255,255,0))
  } 

  // nodes added to the closedSet are drawn gray
  for (var i = 0; i < closedSet.length; i++) {
      closedSet[i].show(color(119,136,153))
  } 

  // shortest path drawn green
  for (var i = 0; i < path.length; i++) {
      path[i].show(color(0,255,0));
  }  
}