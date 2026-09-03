
module.exports = async function (context, req) {
    // Simply return Online status. 
    // The frontend will calculate the User <-> Azure latency.

    context.res = {
        body: {
            region: "Central India",
            status: "Online",
            message: "Azure Function is Active"
        },
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    };
}
