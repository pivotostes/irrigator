let estados = {};

    async function updateStatus() {
      try {
        const sensores = await fetch("/estado_sensores").then(res => res.json());
        const sensoresMap = {
          1: sensores.s1,
          2: sensores.s2,
          3: sensores.s3,
          4: sensores.s4
        };

        for (let i = 1; i <= 4; i++) {
          const valor = Math.min(100, Math.max(0, sensoresMap[i])); // força entre 0–100
          const barra = document.getElementById(`sensor${i}-bar`);
          barra.style.width = `${valor}%`;
          barra.innerText = `${valor}%`;

          // Remove classes antigas
          barra.classList.remove("low", "medium", "high");

          // Adiciona classe com base no valor
          if (valor <= 30) {
            barra.classList.add("low");
          } else if (valor <= 70) {
            barra.classList.add("medium");
          } else {
            barra.classList.add("high");
          }

          const alerta = document.getElementById(`sensor${i}-alert`);
          alerta.classList.remove("low", "medium", "high");

          if (valor <= 30) {
            barra.classList.add("low");
            alerta.classList.add("low");
            alerta.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Seco';
          } else if (valor <= 70) {
            barra.classList.add("medium");
            alerta.classList.add("medium");
            alerta.innerHTML = '<i class="fas fa-water"></i> Moderado';
          } else {
            barra.classList.add("high");
            alerta.classList.add("high");
            alerta.innerHTML = '<i class="fas fa-seedling"></i> Úmido';
          }
        }

        // Busca os estados das bombas
        const estados = await fetch("/estado_bombas").then(res => res.json());

        for (let i = 1; i <= 4; i++) {
          const ligado = estados[i] === 1 || estados[String(i)] === 1;

          const btn = document.getElementById(`bomba${i}`);
          const label = document.getElementById(`bomba${i}-label`);

          if (label) {
            label.textContent = ligado ? `💧 Bomba ${i}` : `❌ Bomba ${i}`;
          }

          if (btn) {
            btn.innerHTML = ligado
              ? '<i class="fas fa-toggle-on"></i> Ligado'
              : '<i class="fas fa-toggle-off"></i> Desligado';
            btn.classList.remove("ligada", "desligada");
            btn.classList.add(ligado ? "ligada" : "desligada");
          }
        }
      } catch (err) {
        console.error("Erro ao atualizar status da bomba:", err);
      }

    }

    async function togglePump(id) {
      const novoEstado = estados[id] === 1 ? 0 : 1;

      try {
        const response = await fetch(`/estado_bombas/${id}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ estado: novoEstado })
        });

        if (!response.ok) {
          throw new Error("Erro ao atualizar estado da bomba");
        }

        // Atualiza interface após mudar o estado
        await updateStatus();
      } catch (err) {
        console.error("Erro ao alternar bomba:", err);
      }
    }

    setInterval(updateStatus, 2000);
    window.onload = updateStatus;
