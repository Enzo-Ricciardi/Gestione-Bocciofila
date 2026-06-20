<?php
/**
 * Gestione Bocciofila
 * License: MIT
 *
 * This public version is distributed as a free application and does not
 * require paid licenses or activation codes.
 */
header('Content-Type: application/json');

echo json_encode([
    'isValid' => true,
    'clubName' => 'Gestore Bocciofila',
    'type' => 'FREE',
    'message' => 'Applicazione gratuita: nessuna licenza richiesta.',
    'expiryDate' => null
]);
exit;
?>
