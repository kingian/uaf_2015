import javax.activation.DataHandler;
import javax.activation.DataSource;
import javax.activation.FileDataSource;
import javax.mail.*;
import javax.mail.internet.*;
import java.io.UnsupportedEncodingException;
import java.util.Properties;

/**
 * Created by davidkemker on 6/25/15.
 */
public class Emailer
{
	static final String EMAIL_FROM_ADDRESS = "uaf2015bt@gmail.com";
	static final String EMAIL_PASSWORD = "MCLmRhtW2KJUtzSMzZzB";
	static final String EMAIL_SUBJECT = "UAF 2015 - Bullet Time";
	static final String EMAIL_BODY = "Thanks for stopping by and visiting us at the UAF this year.\nCome see us again next year and we hope you have enjoyed the show!";
	static final String EMAIL_SERVER = "smtp.gmail.com";
	static final int EMAIL_PORT = 587;

	static InternetAddress[] unicodifyAddresses(String addresses) throws AddressException
	{
		InternetAddress[] recipent = InternetAddress.parse(addresses, false);
		for(int i=0; i<recipent.length; i++)
		{
			try
			{
				recipent[i] = new InternetAddress(recipent[i].getAddress(), recipent[i].getPersonal(), "utf-8");
			}
			catch(UnsupportedEncodingException uee)
			{
				throw new RuntimeException("utf-8 not valid encoding?", uee);
			}
		}
		return recipent;
	}

	public static void sendEmail(String emailAddress, String gifPath)
	{
		System.out.println("Attempting to send an email to: "+emailAddress);

		Properties props = new Properties();
		props.put("mail.smtp.auth", "true");
		props.put("mail.smtp.starttls.enable", "true");
		props.put("mail.smtp.host", EMAIL_SERVER);
		props.put("mail.smtp.port", EMAIL_PORT);

		Session mailSession = Session.getInstance(
				props,
				new Authenticator()
				{
					@Override
					protected PasswordAuthentication getPasswordAuthentication()
					{
						return new PasswordAuthentication(EMAIL_FROM_ADDRESS, EMAIL_PASSWORD);
					}
				}
		);


		try
		{
			Message message = new MimeMessage(mailSession);
			message.setFrom(new InternetAddress(EMAIL_FROM_ADDRESS));
			message.setRecipients(
					Message.RecipientType.TO,
					unicodifyAddresses(emailAddress));
			message.setSubject(EMAIL_SUBJECT);

			BodyPart body = new MimeBodyPart();
			MimeMultipart multipart = new MimeMultipart();
			DataSource source = new FileDataSource(gifPath);

			body.setText(EMAIL_BODY);
			body.setDataHandler(new DataHandler(source));
			body.setFileName(gifPath);
			multipart.addBodyPart(body);

			message.setContent(multipart);

			Transport.send(message);

			System.out.println("Email sent.");

		}
		catch (MessagingException e)
		{
			throw new RuntimeException(e);
		}

	}
}
