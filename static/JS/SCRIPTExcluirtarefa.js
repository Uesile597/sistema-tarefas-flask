document.getElementById("excluir").addEventListener("click", function (e) {
    e.preventDefault();

    const selecionados = document.querySelectorAll(
        'input[name="tarefas_selecionadas"]:checked'
    );
    
    if (selecionados.length === 0) {
        alert("Selecione pelo menos uma tarefa !");
        return;
    }

    const ids = Array.from(selecionados).map(cb => cb.value);

    if (!confirm("Tem certeza que deseja excluir esta tarefa ?"))
        return

    fetch("/EXCLUIRTAREFA/excluir", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id_tarefa: ids })
    })

    .then(res => res.json())
    .then(data => {
        alert(data.mensagem);
        location.reload();
    })

    .catch(err => {
        console.error(err);
        alert("Erro ao excluir tarefas .");
    });
});