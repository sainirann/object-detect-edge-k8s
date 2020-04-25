const express = require('express');
const app = express();
const nodemailer = require("nodemailer");

/**
 * User details object
 */
const userDetails = {
    email: "emilia.batz@ethereal.email"
};

/**
 * Sends email notification to the user
 */
app.post('/send_notification', async function(req, res) {


    let transporter = nodemailer.createTransport({
        host: "smtp.ethereal.email",
        port: 587,
        secure: false,
        auth: {
            user: "emilia.batz@ethereal.email",
            pass: "arJYZdR8UfdrYknHCZ"
        }
    });

    let info = await transporter.sendMail({
        from: userDetails.email,
        to: userDetails.email,
        subject: "test Email",
        text: "Hi, \n\nNeed immediate attention!! Suspicicous activity is found. Please take necessary actions. \nThanks and Regards, \nObject Detection Team",
        html: "<p>Hi, <br/><br/>Need immediate attention!! Suspicicous activity is found. Please take necessary actions. <br/><br/>Thanks and Regards,<br/>Object Detection Team<\p>"
    });

    console.log("Message sent: %s", info.messageId);
    console.log("Preview URL: %s", nodemailer.getTestMessageUrl(info));

    return res.status(200).json({ email: userDetails.email });
});

const server = app.listen(3000, "0.0.0.0", function () {
   let host = server.address().address;
   let port = server.address().port;
   console.log("Listening port: ", port);
})
