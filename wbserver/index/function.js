var coopInfo = [{ name: "", tags: [] }, { name: "", tags: [] }, { name: "", tags: [] }, { name: "", tags: [] }, { name: "", tags: [] }];
var funcChoose;
var valueCount;

function initFunc() {
  valueCount = 0;
  for(var i = 0; i< 21; i++){
    var inputField = document.getElementById('Input-' + i);
    inputField.style.display = "none";
  }
}

function searchFunc() {
  var titleTxt = document.getElementById('title');
  var formBox = document.getElementById('form-box');
  var searchField = document.getElementById('search-field');
  var searchInfo = document.getElementById('search-info');
  var hintTxt = document.getElementById('hint-txt');

  var searchString = searchField.value;
  var coopStrings = searchString.split(",");
  for (var i = 0; i < 5; i++)
    coopInfo[i].name = coopStrings[i];

  var tags = [];
  if(funcChoose == 0){  // 查询功能
    console.log(coopStrings);
    $.post("https://www.chival.xyz:444/tags",
      {
        "entnames": searchString
      },
      function (data, status) {
        //alert("数据: \n" + data + "\n状态: " + status);
        //这里获取到了tags的数据是一个json格式的字典，key是entname，value是一个标签数组
        tags = JSON.parse(data);
        console.log(status);
        console.log(tags);

        for (var i = 0; i < 5; i++) {
          if (coopInfo[i].name != undefined) {
            for (var j = 0; j < 6; j++) {
              coopInfo[i].tags[j] = tags[coopStrings[i]][j];
            }
          }
        }

      }
    );  // 查询功能结束
  } else if(funcChoose == 1){   // 预测功能

  }
  tabFunc(1);


  if(coopInfo[0].name){
    titleTxt.style.display = "none";
    formBox.style.top = "25%";
    searchField.placeholder = "在此输入公司名称...";
    searchInfo.style.display = "block";
    hintTxt.style.display = "none";
  } else if(funcChoose == 0)
    hintTxt.innerHTML = "请输入公司名称";
    else
    coopInfo[0].name = "预测结果";

  for (var i = 0; i < 5; i++)
    document.getElementById('coop' + (i + 1)).innerText = (coopInfo[i].name == undefined ? "" : '结果' + (i + 1));

}

function clearFunc() {
  funcChoose = 0;

  var searchField = document.getElementById('search-field');
  var searchBtn = document.getElementById('search-btn');
  var formBox = document.getElementById('form-box');
  var searchInfo = document.getElementById('search-info');
  var hintTxt = document.getElementById('hint-txt');
  var valueBox = document.getElementById('valueBox');

  searchField.placeholder = "";
  searchBtn.disabled = "";
  formBox.style.top = "34%";
  searchInfo.style.display = "none";
  hintTxt.innerHTML = "输入多个公司名称时请用逗号隔开，同时查询最多支持5个公司。"
  hintTxt.style.display = "block";
  valueBox.style.display = "none";
}

function closeFunc() {
  var titleTxt = document.getElementById('title');
  var searchField = document.getElementById('search-field');
  var searchBtn = document.getElementById('search-btn');
  var formBox = document.getElementById('form-box');
  var searchInfo = document.getElementById('search-info');
  var hintTxt = document.getElementById('hint-txt');
  var valueBox = document.getElementById('valueBox');

  titleTxt.style.display = "block";
  searchField.placeholder = "在此输入公司名称...";
  searchField.value = "";
  searchBtn.disabled = "disabled";
  formBox.style.top = "35%";
  searchInfo.style.display = "none";
  hintTxt.style.display = "none";
  valueBox.style.display = "none";
}

function tabFunc(index) {

  for (var i = 0; i < 5; i++)
    document.getElementById('coop' + (i + 1)).style.color = (i == index - 1) ? "#ffffff" : "rgba(255, 255, 255, 0.6)";

  document.getElementById('coopName').innerText = coopInfo[index - 1].name;
  if (coopInfo[index - 1].name) {
    for (var i = 0; i < 6; i++) {
      document.getElementById('tag' + (i + 1)).innerText = "标签" + (i + 1) + "：" + ((coopInfo[index - 1].tags[i] == undefined) ? "xxxxxxx" : coopInfo[index - 1].tags[i]);
    }
  }
}

function predictFunc() {
  funcChoose = 1;

  var predictHint = document.getElementById('predict-hint');
  var searchField = document.getElementById('search-field');
  var formBox = document.getElementById('form-box');
  var searchInfo = document.getElementById('search-info');
  var hintTxt = document.getElementById('hint-txt');
  var valueBox = document.getElementById('valueBox');

  predictHint.style.display = "none";
  searchField.value = "";
  formBox.style.top = "34%";
  searchInfo.style.display = "none";
  hintTxt.innerHTML = ""
  hintTxt.style.display = "block";
  valueBox.style.display = "block";
}

function addFunc() {
  var valueBoxToShow = document.getElementById('Input-' + (valueCount++));
  valueBoxToShow.style.display = "block";
  if(valueCount >= 10) {
    var background = document.getElementById('background');

  }
}

function changeFunc(index) {

}
