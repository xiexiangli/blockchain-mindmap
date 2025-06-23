
<!-- saved from url=(0056)file:///Users/mac/Downloads/blockchain_canvas%20(1).html -->
<html lang="zh-CN"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body>```html



  
  <title>哈希值在区块链中的作用示意图</title>
  <style>
    body {
      margin: 0; padding: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      background: #f0f4f8;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }
    h2 {
      margin: 1rem;
    }
    canvas {
      border: 1px solid #ccc;
      background: #fff;
    }
    button {
      margin: 1rem;
      padding: 0.5rem 1rem;
      font-size: 16px;
      cursor: pointer;
    }
  </style>


  <h2>哈希值在区块链中的作用示意图</h2>
  <canvas id="hashChain" width="900" height="380"></canvas>
  <button id="tamperBtn">模拟篡改第2个区块数据</button>

  <script>
    const canvas = document.getElementById("hashChain");
    const ctx = canvas.getContext("2d");

    // 基本参数
    const blockW = 180, blockH = 110;
    const startX = 50, startY = 120;
    const gap = 240;

    // 区块示意数据
    let blocks = [
      {index: 0, data: "交易数据A", hash: "AAA123", prevHash: "---", valid: true},
      {index: 1, data: "交易数据B", hash: "BBB456", prevHash: "AAA123", valid: true},
      {index: 2, data: "交易数据C", hash: "CCC789", prevHash: "BBB456", valid: true},
    ];

    // 绘制单个区块
    function drawBlock(block, x, y) {
      ctx.lineWidth = 3;
      ctx.strokeStyle = block.valid ? "#4CAF50" : "#E53935";
      ctx.fillStyle = block.valid ? "#A5D6A7" : "#EF9A9A";
      ctx.fillRect(x, y, blockW, blockH);
      ctx.strokeRect(x, y, blockW, blockH);

      ctx.fillStyle = "#000";
      ctx.font = "bold 16px monospace";
      ctx.fillText("区块 #" + block.index, x + 10, y + 25);

      ctx.font = "14px monospace";
      ctx.fillText("数据: " + block.data, x + 10, y + 50);
      ctx.fillText("哈希: " + block.hash, x + 10, y + 75);
      ctx.fillText("前哈希: " + block.prevHash, x + 10, y + 100);
    }

    // 画箭头，表示链链接
    function drawArrow(fromX, fromY, toX, toY, valid = true) {
      const headLen = 12;
      const dx = toX - fromX;
      const dy = toY - fromY;
      const angle = Math.atan2(dy, dx);

      ctx.strokeStyle = valid ? "#4CAF50" : "#E53935";
      ctx.fillStyle = valid ? "#4CAF50" : "#E53935";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(fromX, fromY);
      ctx.lineTo(toX, toY);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(toX, toY);
      ctx.lineTo(
        toX - headLen * Math.cos(angle - Math.PI / 6),
        toY - headLen * Math.sin(angle - Math.PI / 6)
      );
      ctx.lineTo(
        toX - headLen * Math.cos(angle + Math.PI / 6),
        toY - headLen * Math.sin(angle + Math.PI / 6)
      );
      ctx.lineTo(toX, toY);
      ctx.fill();
    }

    // 文字说明
    function drawLabels() {
      ctx.fillStyle = "#333";
      ctx.font = "18px sans-serif";
      ctx.fillText("1. 区块数据生成唯一哈希值", 20, 30);
      ctx.fillText("2. 每个区块包含前一区块的哈希，形成链条", 20, 60);
      ctx.fillText("3. 篡改区块数据会导致哈希变化，破坏链的完整性", 20, 90);
    }

    // 重新计算链条有效性
    function recalcValidity() {
      blocks.forEach((b, i) => {
        if (i === 0) {
          b.valid = true; // 第一个区块默认有效
        } else {
          // 校验前哈希是否和前区块哈希匹配
          b.valid = b.prevHash === blocks[i - 1].hash && blocks[i - 1].valid;
        }
      });
    }

    // 模拟数据哈希更新（简化版，实际用复杂哈希函数）
    function fakeHash(data) {
      // 取字符串字符编码和长度构造简易伪哈希
      let sum = 0;
      for (let i = 0; i < data.length; i++) {
        sum += data.charCodeAt(i);
      }
      return (data[0].toUpperCase() + sum.toString(16).toUpperCase()).slice(0,6);
    }

    // 重新计算哈希和前哈希关联
    function recalcHashes() {
      blocks[0].hash = fakeHash(blocks[0].data);
      for (let i = 1; i < blocks.length; i++) {
        blocks[i].prevHash = blocks[i - 1].hash;
        blocks[i].hash = fakeHash(blocks[i].data);
      }
    }

    // 主绘制函数
    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawLabels();

      for (let i = 0; i < blocks.length; i++) {
        const x = startX + i * gap;
        drawBlock(blocks[i], x, startY);

        if (i > 0) {
          drawArrow(
            x,
            startY + blockH / 2,
            x - 30,
            startY + blockH / 2,
            blocks[i].valid
          );
        }
      }
    }

    // 初始化画面
    recalcHashes();
    recalcValidity();
    draw();

    // 模拟篡改数据按钮事件
    document.getElementById("tamperBtn").addEventListener("click", () => {
      blocks[1].data = blocks[1].data === "交易数据B" ? "篡改的数据！" : "交易数据B";
      recalcHashes();
      recalcValidity();
      draw();
    });
  </script>


```

</body></html>
