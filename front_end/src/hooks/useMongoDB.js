// const { MongoClient } = require("mongodb");
// // Replace the uri string with your connection string.
// const uri = 'mongodb://cosmosdbcolumbiacapstonefall2022:alv0mZxNDjmu37OvR0USNaFrT694JwXE8qpdmb62KSRhHZbZIHaiIw7KqceRlSwFRmhhqFCfdtCKDEnWXh9w8Q==@cosmosdbcolumbiacapstonefall2022.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmosdbcolumbiacapstonefall2022@';
// const client = new MongoClient(uri);
// async function run() {
//   try {
//     const database = client.db('pubmed');
//     const movies = database.collection('abstracts');
//     const query = { title: 'Back to the Future' };
//     const movie = await movies.findOne(query);
//     console.log(movie);
//   } finally {
//     // Ensures that the client will close when you finish/error
//     await client.close();
//   }
// }
// run().catch(console.dir);

