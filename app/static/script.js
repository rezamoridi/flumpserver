const ball = document.getElementById('ball');
let posX = 0;
let posY = 0;
let directionX = 2; // Speed in the X direction
let directionY = 2; // Speed in the Y direction

function moveBall() {
    // Update the position of the ball
    posX += directionX;
    posY += directionY;

    // Check for collision with the window edges
    if (posX + ball.clientWidth >= window.innerWidth || posX <= 0) {
        directionX = -directionX; // Reverse direction on X-axis
    }
    if (posY + ball.clientHeight >= window.innerHeight || posY <= 0) {
        directionY = -directionY; // Reverse direction on Y-axis
    }

    // Apply the new position to the ball
    ball.style.transform = `translate(${posX}px, ${posY}px)`;

    // Call the function again on the next frame
    requestAnimationFrame(moveBall);
}

// Start moving the ball
moveBall();