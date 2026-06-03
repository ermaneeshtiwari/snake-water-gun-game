const choices = { S: 1, W: 0, G: -1 };
const names = { 1: 'Snake', 0: 'Water', -1: 'Gun' };

const buttons = document.querySelectorAll('.choices button');
const status = document.getElementById('status');
const detail = document.getElementById('detail');
const resetBtn = document.getElementById('reset');

function computerPick() {
  const keys = Object.keys(choices);
  return keys[Math.floor(Math.random() * keys.length)];
}

function play(userChoice) {
  const comp = computerPick();
  if (!choices.hasOwnProperty(userChoice)) {
    status.textContent = 'Invalid choice';
    detail.textContent = '';
    return;
  }

  if (userChoice === comp) {
    status.textContent = "It's a tie!";
    detail.textContent = `You: ${userChoice} — Computer: ${comp}`;
    return;
  }

  const u = choices[userChoice];
  const c = choices[comp];

  if ((u === choices['S'] && c === choices['W']) ||
      (u === choices['W'] && c === choices['G']) ||
      (u === choices['G'] && c === choices['S'])) {
    status.textContent = 'You win!';
  } else {
    status.textContent = 'Computer wins!';
  }
  detail.textContent = `You: ${userChoice} (${names[u]}) — Computer: ${comp} (${names[c]})`;
}

buttons.forEach(b => b.addEventListener('click', () => play(b.dataset.choice)));
resetBtn.addEventListener('click', () => { status.textContent = 'Make a choice to play.'; detail.textContent = ''; });
