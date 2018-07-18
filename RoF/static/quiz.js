const numQ=20;
var nRight, nWrong, acc, dataLen, turn;
var dataset, tableStr, ldbTableStr="";
var userName="Anon";
var quizData=[];
var ldbData=[];
var isValidName = false;

function validateName() {
  userName = $("input[name=user-name]").val();
  if (userName == "") {
    $('#name-check').html(`<= <i>C'mon bruh...</i>`);
  } else {
    $('#name-check').html("");
    isValidName = true;
  }
}

function startGame(name) {
  userName = $("input[name=user-name]").val();
  if (userName == "") {
    $('#name-check').html(`<font color='red'><= <i>C'mon bruh...</font></i>`);
  } else {
    dataset=name;
    $.getJSON("/labels_meta", function(data) {
      dataLen=data[dataset].shape;
      let infoDataset = `<i>(Source: <a href=${data[dataset].source}>${data[dataset].name}</a>)</i>`;
      $('#info-dataset').html(infoDataset);
      $(".start-screen").toggle();
      $(".quiz-screen").toggle();
      newGame();
    });
    $('#name-check').html("");
  }
}






function getAccuracy(nRight, nWrong) {
  if (nRight+nWrong == 0){return 0;}
  else {return (nRight/(nRight+nWrong)*100).toFixed(2);}
}

function updateScore() {
  acc = getAccuracy(nRight, nWrong);
  $('#qn-number').html('Question: '+(turn+1)+'/'+numQ);
  $('#scr-correct').html('Correct: '+nRight);
  $('#scr-incorrect').html('Incorrect: '+nWrong);
  $('#scr-accuracy').html('Score: '+acc+' %'); 
}
function guess(guessInt) {
  quizData[turn].guess = guessInt;
  quizData[turn].correct = (quizData[turn].guess == quizData[turn].truth);
  if (quizData[turn].truth == guessInt) {
    $('#ans-status').html("<font color='green'>Correct!</font>");
    nRight+=1;
    nextOrEnd();
  } else {
    let wrongResp = (guessInt == 1) ? "fake.":"real.";
    $('#ans-status').html("<font color='red'>Wrong - It's "+wrongResp+"</font>");
    nWrong+=1;
    nextOrEnd();
  }
}
function nextOrEnd() {
  if (turn == numQ-1) {
    updateScore();
    endGame();
  } else {
    nextIter();
  }
}
function endGame() {
  let endLog;
  if (acc <= 5) {endLog="OMEGALUL3DXDXDXD!!1!! <br/>Y";} else
  if (acc <= 20) {endLog="Almost there... I know you want it... <br/>Y";} else
  if (acc <= 30) {endLog="LUL3D, <br/>Y";} else
  if (acc <= 40) {endLog="LUL,<br/>Y" ;} else
  if (acc <= 50) {endLog="Okay "+userName+",<br/>y";} else
  if (acc <= 60) {endLog="Cool "+userName+",<br/>y";} else
  if (acc <= 70) {endLog="That's pretty good "+userName+",<br/>y";} else
  if (acc <= 80) {endLog="Wow you're really good at this "+userName+",<br/>y";} else
  if (acc <= 95) {endLog="GG "+userName+"!<br/>Y"; } else {endLog="XD NICE CHEAT U GOT THERE M8,<br/>Y";}
  $('#end-message-head').html(endLog+"our score is "+acc+" % <i>(Dataset: "+dataset+")");
  $(".quiz-screen").toggle();
  scoreTable();
  createTable();
  $(".end-screen").toggle();
  appendQuiz();
}
function mainMenu() {
  quizData = [];
  turn = -1;
  nRight, nWrong=0;
  updateScore();
  $('#ans-status').html("");
  $('#scr-table').html(""); 
  $(".end-screen").toggle();
  $(".start-screen").toggle();
}

function getComment() {
  $('#cmt-line').html(`<b>${quizData[turn].line}</b>`);
}
function nextIter() {
  turn++;
  getComment();
  updateScore();
}
function newGame() {
  turn=-1;
  nRight=0;
  nWrong=0;
  idxList=d3.shuffle(d3.range(0,dataLen,1)).slice(0,numQ);
  console.log('userName:'+userName,'dataset:'+dataset,'dataLen:'+dataLen,'IDs:'+idxList);
  for (i = 0; i < numQ; i++) {
    let rowIdx = idxList[i];
    $.getJSON("/labels/"+dataset+"/"+rowIdx, function(data) {
        let rowData = {user_name: userName,
                      dataset: dataset,
                      index:data.index,
                      line:data.line,
                      truth:data.truth}
        quizData.push(rowData);
        if (quizData.length == 1) {
          nextIter();
        }
    });
  }
}
function scoreTable() {
  tableStr = "<h4><font color='green'>Correct: "+nRight+"</font><font color='red'> Wrong: "+nWrong+"</font></i></h4>";
  // Table header
  let headerKeys = ["#","Line","Guess","Truth","Correct"]
  tableStr += "<table border==\"10\"><tr>";
  for (let i=0; i<headerKeys.length; i++) {
    tableStr += '<td>' + headerKeys[i] + '</td>';
  }
  tableStr += "</tr>";
  // Table rows
  let keys = ["line","guess","truth","correct"];
  for (let i=0; i<quizData.length; i++) {
    tableStr += '<tr>';
    if (quizData[i].correct==1) {
      tableStr += '<td><font color="green">' + parseInt(i+1) + '</font></td>';
      for (let j=0; j<keys.length; j++) {
        tableStr += '<td><font color="green">' + quizData[i][keys[j]] + '</font></td>';
      }
    } else {
      tableStr += '<td><font color="red">' + parseInt(i+1) + '</font></td>';
      for (let j=0; j<keys.length; j++) {
        tableStr += '<td><font color="red">' + quizData[i][keys[j]] + '</font></td>';
      }
    }
    tableStr += '</tr>';
  }
  tableStr += "</table>";
}
function createTable() {
  ldbTable(datasetName="pop_mag");
  $('#scr-table').html(tableStr); 
  $('#ldb-table').html(ldbTableStr); 
}
function toggleTable(tableName) {
  $('#'+tableName).toggle();
}
function appendQuiz() {
  // construct an HTTP request
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/append_quiz', true);
  xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  // send the collected data as JSON
  xhr.send(JSON.stringify({data:quizData}));
  console.log('Quiz Appended.')
}
