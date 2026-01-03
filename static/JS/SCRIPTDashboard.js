//script para modal-contents
    const botoesabrir = document.querySelectorAll(".btn-info");
    const modais = document.querySelectorAll(".meu-modal");

    botoesabrir.forEach((botao, index) => {
        botao.onclick = () => {
            modais[index].showModal();
        };
    });

    modais.forEach((modal) => {
        modal.addEventListener("click", (event) => {
            if(event.target === modal) {
                modal.close();
            }
        });
    });
//script para modal-contents

//script para gráfico de pizza
    const dados_pizza = JSON.parse(
        document.getElementById("dados-pizza").textContent
    );
    const canvas_pizza = document.getElementById('graficoStatus');

    const coresPorLabel = {
        "concluida": '#008000a2',
        "pendente": '#ff0000a2',
        "em andamento": '#FFFF00a2'
    };
    const cores = dados_pizza.labels.map(
        label => coresPorLabel[label] || '#999'
    );

    if (canvas_pizza) {
        new Chart(canvas_pizza, {
            type: 'pie',
            data: {
                labels: dados_pizza.labels,
                datasets: [{
                    data: dados_pizza.valores,
                    backgroundColor: cores
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffffff',
                            font: {
                                size: 18,
                                family: 'Arial'
                            }
                        }
                    }
                }
            }
        });
    }
    
//script para gráfico de pizza

//script para gráfico de barras
    const dados_barras = JSON.parse(
        document.getElementById('dados-barras').textContent
    );
    const canvas_barras = document.getElementById('graficoBarras');

    if (canvas_barras) {
        new Chart(canvas_barras, {
            type: 'bar',
            data: {
                labels: dados_barras.labels,
                datasets: [{
                    label: "Quantidade de Tarefas",
                    data: dados_barras.valores,
                    backgroundColor: [
                        '#ffffffa2',
                        '#008000a2'
                    ]
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffffff',
                            font: {
                                size: 18,
                                family: 'Arial'
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: '#ffffffff',
                            font: {
                                size: 18,
                                family: 'Arial'
                            }
                        },
                        grid: {
                            color: '#c0bfbfff'
                        }
                    },

                    y: {
                        ticks: {
                            color: '#ffffffff',
                            font: {
                                size: 18,
                                family: 'Arial'
                            }
                        },
                        grid: {
                            color: '#c0bfbfff'
                        }
                    }
                }
            }
        });
    }
//script para gráfico de barras