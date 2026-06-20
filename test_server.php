<?php
/**
 * Gestione Bocciofila
 * License: MIT
 *
 * Optional server write-permission diagnostic used during deployment.
 */
$dir = __DIR__ . '/activations';
echo "Verifica cartella: $dir<br>";
if (!file_exists($dir)) {
    echo "Cartella NON esiste. Provo a crearla...<br>";
    mkdir($dir, 0777, true);
}
if (is_writable($dir)) {
    echo "Cartella SCRIVIBILE! ✅<br>";
    $testFile = $dir . '/test_'.time().'.txt';
    if (file_put_contents($testFile, "Test Scrittura " . date('Y-m-d H:i:s'))) {
        echo "File di prova creato con successo! ✅<br>";
        echo "Contenuto: " . file_get_contents($testFile);
    } else {
        echo "Errore nella creazione del file. ❌";
    }
} else {
    echo "Cartella NON scrivibile. ❌ Contatta l'assistenza o cambia i permessi via FTP.";
}
?>
