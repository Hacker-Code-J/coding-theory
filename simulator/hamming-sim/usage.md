HAMMING ALGEBRAIC LAB - USAGE GUIDE

1. SETUP:
   - Place index.html, style.css, and script.js in one folder.
   - Open index.html in any modern web browser.
   - Ensure you have an internet connection (to load Tailwind/KaTeX via CDN).

2. WORKFLOW:
   - SENDER: Click the 4 bits in Step 1 to set your message (Data Vector d).
     The math updates to show the Encoding transformation (c = d * G).
   
   - CHANNEL: Click any bit in the dark central column. This simulates noise
     by flipping a bit. The bit will turn red to show an error was injected.
   
   - RECEIVER: Watch the Syndrome (s) calculation. If s is non-zero, it means
     the vector r is no longer in the null space of H.
   
   - DIAGNOSIS: Look at the Syndrome vector result. It will match exactly ONE 
     of the columns in the H matrix. The index of that column is the 
     location of the flipped bit.

3. UNDERSTANDING GF(2):
   - All additions are XOR.
   - All multiplications are AND.
   - Hamming(7,4) can correct exactly 1 bit error. If you flip 2 bits, 
     the simulator will show a "false" correction or a valid state.
