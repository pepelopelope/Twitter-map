// Configura el cliente de DynamoDB
var dynamodb = new AWS.DynamoDB({region: 'NOMBRE_DE_TU_REGION'});

// Obtiene el stream de la tabla de DynamoDB
var params = {
    StreamArn: 'ARN_DE_TU_STREAM', // El ARN del stream de la tabla de DynamoDB
    Limit: 100 // El número máximo de registros que se pueden obtener en cada solicitud
};
dynamodb.describeStream(params, function(err, data) {
    if (err) console.log(err, err.stack);
    else {
        // Obtiene el último registro del stream
        var shardId = data.StreamDescription.Shards[0].ShardId;
        var params = {
            ShardId: shardId,
            ShardIteratorType: 'LATEST',
            StreamArn: 'ARN_DE_TU_STREAM'
        };
        dynamodb.getShardIterator(params, function(err, data) {
            if (err) console.log(err, err.stack);
            else {
                var shardIterator = data.ShardIterator;
                // Itera sobre los registros del stream
                setInterval(function() {
                    dynamodb.getRecords({ShardIterator: shardIterator}, function(err, data) {
                        if (err) console.log(err, err.stack);
                        else {
                            // Itera sobre los registros
                            for (var i = 0; i < data.Records.length; i++) {
                                var record = data.Records[i];
                                // Convierte la cadena JSON en un objeto JavaScript
                                var tweet = AWS.DynamoDB.Converter.unmarshall(record.dynamodb.NewImage);
                                // Crea un marcador en el mapa para cada tweet con coordenadas
                                if (tweet.coordinates) {
                                    var marker = L.marker([tweet.coordinates[1], tweet.coordinates[0]]).addTo(map);
                                    marker.bindPopup(tweet.text);
                                }
                            }
                            // Actualiza el iterador del shard para obtener nuevos registros
                            shardIterator = data.NextShardIterator;
                        }
                    });
                }, 5000); // Intervalo de 5 segundos para actualizar los registros
            }
        });
    }
});
