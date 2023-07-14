const svgElement = document.getElementById('marca_grafica',);

// Define a posição inicial do elemento
let posicaoAtual = 0;

// Define a velocidade e a amplitude do balanço
const velocidade = 0.03; // ajuste conforme necessário9
const amplitude = 3; // ajuste conforme necessário

// Função para atualizar a posição horizontal do elemento
function atualizarPosicao() {
    // Calcula a nova posição baseada no tempo e na amplitude
    const novaPosicao = Math.sin(posicaoAtual) * amplitude;

    // Aplica a transformação de translação horizontal ao elemento SVG
    svgElement.setAttribute('transform', `translate(${novaPosicao}, 0)`);

    // Atualiza a posição atual
    posicaoAtual += velocidade;

    // Chama a função novamente na próxima animação
    requestAnimationFrame(atualizarPosicao);
}
atualizarPosicao();