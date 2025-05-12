<?php
$sensores_file = "sensores.txt";
$bombas_file = "bomba_estado.txt";

// Se for uma requisição para salvar sensores
if ($_SERVER["REQUEST_METHOD"] == "GET" && isset($_GET['s1']) && isset($_GET['s2']) && isset($_GET['s3']) && isset($_GET['s4'])) {
    $dados = json_encode([
        "s1" => intval($_GET['s1']),
        "s2" => intval($_GET['s2']),
        "s3" => intval($_GET['s3']),
        "s4" => intval($_GET['s4'])
    ]);
    file_put_contents($sensores_file, $dados);
    echo "Sensores Atualizados";
    exit;
}

// Se for uma requisição para mudar o estado da bomba
if ($_SERVER["REQUEST_METHOD"] == "GET" && isset($_GET['bomba']) && isset($_GET['estado'])) {
    $bomba = intval($_GET['bomba']);
    $estado = intval($_GET['estado']);

    $estados = json_decode(file_get_contents($bombas_file), true);
    $estados[$bomba] = $estado;

    file_put_contents($bombas_file, json_encode($estados));
    echo "Bomba $bomba " . ($estado ? "Ligada" : "Desligada");
    exit;
}

// Se nenhuma requisição for reconhecida, retorna erro
http_response_code(400);
echo "Requisição inválida";
?>
