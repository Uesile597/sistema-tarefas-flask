const botao_menu = document.querySelector('.botao-menu')
const menu_lateral = document.querySelector('.menu-lateral')
const conteudo = document.querySelector('.conteudo')
const background = document.querySelector('.background')
const caixa1 = document.querySelector('.caixa1')
const topo = document.querySelector('.topo')

botao_menu.addEventListener('click', () => {
    menu_lateral.classList.toggle('ativo')
    botao_menu.classList.toggle('ativo')
    conteudo.classList.toggle('ativo')
    background.classList.toggle('ativo')
    caixa1.classList.toggle('ativo')
    topo.classList.toggle('ativo')
})

background.addEventListener('click', () => {
    menu_lateral.classList.remove('ativo')
    botao_menu.classList.remove('ativo')
    conteudo.classList.remove('ativo')
    background.classList.remove('ativo')
    caixa1.classList.remove('ativo')
    topo.classList.remove('ativo')
})
