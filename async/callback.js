// 最基础的回调函数

function fetchData(callback) {
    // setTimeout 是一个 非阻塞-异步进程: 非阻塞地持续1000毫秒，这个过程中让出cpu；1000毫秒后发出通知，抢回cpu，然后运行回调函数callback 
    setTimeout(() => {
        console.log("数据获取完成");
        const data = { name: "Alice" };
        callback(data); // 调用回调函数
    }, 1000);
}

function process(data) {
    console.log("处理数据:", data.name);
}

fetchData(process); // 把 process 函数作为回调传进去
console.log("主程序继续")



// 稍复杂的回调
// 一个异步文件读取函数
function readFileAsync(delay, filePath, callback) {
  console.log(`开始读取文件：${filePath}`);

  setTimeout(() => {
    const fileContent = `这是从 ${filePath} 读取到的内容。`;
    const error = null; // 没有错误

    // 文件读取完成后，调用传入的回调函数
    if (error) {
      callback(error, null); // 如果有错误，将错误作为第一个参数传递
    } else {
      callback(null, fileContent); // 如果成功，将null作为第一个参数，内容作为第二个参数传递
    }
  }, delay); // 延迟 delay 毫秒
}

// 定义一个回调函数来处理文件读取的结果
function handleFileRead(err, data) {
  if (err) {
    console.error("文件读取失败：", err);
    return;
  }
  console.log("文件读取成功！");
  console.log("文件内容：", data);
  console.log("--------------------");
}



// 两个异步操作
console.log("主程序开始执行...");

readFileAsync(1000, "readme.txt", handleFileRead); // 第一个异步操作

console.log("主程序继续执行，不会等待文件读取完成...");

readFileAsync(2000, "config.json", handleFileRead); // 第二个异步操作

console.log("主程序执行完毕？不，等待异步操作完成...");







// 回调地狱
// 异步操作中，存在串行顺序执行
// 读取文件，写入文件，打印已写入的文件。三个异步操作顺序执行：每一个异步操作只有在前一个操作执行后才能执行

// readFileAsync(delay, filePath_r, callback);
// writeFileAsync(delay, filePath_w, callback);
// printFileAsync(delay, filePath_w, callback);

// writeFileAsync 应该是 readFileAsync 的 callback 的一部分, 而 printFileAsync 应该是 writeFileAsync 的 callback 的一部分
// 这就是嵌套回调