<?php return array(
    'root' => array(
        'name' => 'kauan/modulodelogistica',
        'pretty_version' => '1.0.0+no-version-set',
        'version' => '1.0.0.0',
        'reference' => null,
        'type' => 'project',
        'install_path' => __DIR__ . '/../../',
        'aliases' => array(),
        'dev' => true,
    ),
    'versions' => array(
        'kauan/modulodelogistica' => array(
            'pretty_version' => '1.0.0+no-version-set',
            'version' => '1.0.0.0',
            'reference' => null,
            'type' => 'project',
            'install_path' => __DIR__ . '/../../',
            'aliases' => array(),
            'dev_requirement' => false,
        ),
        'php-amqplib/php-amqplib' => array(
            'pretty_version' => 'v2.8.0',
            'version' => '2.8.0.0',
            'reference' => '7df8553bd8b347cf6e919dd4a21e75f371547aa0',
            'type' => 'library',
            'install_path' => __DIR__ . '/../php-amqplib/php-amqplib',
            'aliases' => array(),
            'dev_requirement' => false,
        ),
        'videlalvaro/php-amqplib' => array(
            'dev_requirement' => false,
            'replaced' => array(
                0 => 'v2.8.0',
            ),
        ),
    ),
);
