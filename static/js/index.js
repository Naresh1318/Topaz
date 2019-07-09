jQuery(document).ready(function($) {

  setTimeout(function() {
    runNetworkAnim();
  }, 500);

  var resizeTimeout;
  window.onresize = function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(runNetworkAnim, 500);
  }

  // convert hex to rgb
  function convertHex(hex,opacity){
      hex = hex.replace('#','');
      r = parseInt(hex.substring(0,2), 16);
      g = parseInt(hex.substring(2,4), 16);
      b = parseInt(hex.substring(4,6), 16);

      result = 'rgba('+r+','+g+','+b+','+opacity/100+')';
      return result;
  }

  var currentGlobalID = -1;

  function runNetworkAnim() {
    var currentScopeID = ++currentGlobalID;
    var canvas = document.querySelector("#network");
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;

    // Only run if canvas is over x px
    //if (canvas.width > 100) {
      var ctx = canvas.getContext("2d");

      var MAIN_COLOR = "#666",
          MAIN_COLOR_RGB = convertHex(MAIN_COLOR,0.5);
          SEC_COLOR = "#404040",
          BORDER_COLOR = "#404040",
          LINE_ALPHA = 100,
          NUM_BALLS = 70, // higher is less
          BALL_RAD = 6, //3
          BALL_RAD_MIN = 2,
          SPEED = 0.3,
          GLOB_ALPHA = 0.5,
          MOUSE_RAD = 100,
          CONN_DIST = 100;
          FPS = 60;

      var TAU = 2 * Math.PI;

      times = [];
      function loop() {
        if (currentGlobalID === currentScopeID ) {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          update();
          draw();
          requestId = requestAnimationFrame(loop);
        }
      }

      function stopAnimation(e) {
          cancelAnimationFrame(requestId);
      }

      function Ball (startX, startY, startVelX, startVelY) {
        this.x = startX || Math.random() * canvas.width;
        this.y = startY || Math.random() * canvas.height;
        this.vel = {
          x: startVelX || Math.random() * SPEED * 2 - SPEED,
          y: startVelY || Math.random() * SPEED *2 - SPEED
        };
        this.update = function(canvas) {
          if (this.x > canvas.width + 50 || this.x < -50) {
            this.vel.x = -this.vel.x;
          }
          if (this.y > canvas.height + 50 || this.y < -50) {
            this.vel.y = -this.vel.y;
          }
          this.x += this.vel.x;
          this.y += this.vel.y;
        };
        this.draw = function(ctx, can) {
          ctx.beginPath();
          var distM = distMouse(this);
          if (distM > MOUSE_RAD) {
            ctx.fillStyle = MAIN_COLOR;
            ctx.globalAlpha =  GLOB_ALPHA;
            ctx.arc((0.5 + this.x) | 0, (0.5 + this.y) | 0, BALL_RAD_MIN, 0, TAU, false);
          } else {
            ctx.fillStyle = SEC_COLOR;
            ctx.strokeStyle= BORDER_COLOR;
            ctx.globalAlpha = 1;
            var BALL_RAD_DYN = (distM > CONN_DIST ? BALL_RAD_MIN : BALL_RAD * (1 - distM / CONN_DIST))
            ctx.arc((0.5 + this.x) | 0, (0.5 + this.y) | 0, BALL_RAD_DYN, 0, TAU, false);
            ctx.stroke();
          }

          ctx.fill();
        }
      }

      var balls = [];
      for (var i = 0; i < canvas.width * canvas.height / (NUM_BALLS*NUM_BALLS); i++) {
        balls.push(new Ball(Math.random() * canvas.width, Math.random() * canvas.height));
      }

      var lastTime = Date.now();
      function update() {
        var diff = Date.now() - lastTime;
        for (var frame = 0; frame * 16.6667 < diff; frame++) {
          for (var index = 0; index < balls.length; index++) {
            balls[index].update(canvas);
          }
        }
        lastTime = Date.now();
      }
      var mouseX = -1e9, mouseY = -1e9;
      document.addEventListener('mousemove', function(event) {
        mouseX = event.clientX;
        mouseY = event.clientY;
      });

      function distMouse(ball) {
        return Math.hypot(ball.x - mouseX, ball.y - mouseY);
      }

      function draw() {
        for (var index = 0; index < balls.length; index++) {
          var ball = balls[index];
          ctx.beginPath();
          for (var index2 = balls.length - 1; index2 > index; index2 += -1) {
            var ball2 = balls[index2];
            var dist = Math.hypot(ball.x - ball2.x, ball.y - ball2.y);
              if (dist < CONN_DIST) {
                var distM = distMouse(ball2);
                var line_alp = 1-(dist/CONN_DIST);
                if (distM > MOUSE_RAD) {
                  ctx.strokeStyle = MAIN_COLOR;
                  ctx.globalAlpha =  ctx.globalAlpha = 1 - (dist > CONN_DIST ? .8 : dist / CONN_DIST);
                } else {
                  //ctx.fillStyle = 'rgba(255,0,0,1)';

                  ctx.strokeStyle = SEC_COLOR;
                  ctx.globalAlpha = 1;
                }
                ctx.moveTo((0.5 + ball.x) | 0, (0.5 + ball.y) | 0);
                ctx.lineTo((0.5 + ball2.x) | 0, (0.5 + ball2.y) | 0);
              }
            }
          ctx.stroke();
          ball.draw(ctx, canvas);
        }
      }

      // Start
      loop();
    //}
    var runNetworkAnimObj = new Object()
    runNetworkAnimObj.stopAnimation = stopAnimation
    return runNetworkAnimObj
  }
  Multi = new runNetworkAnim();

});