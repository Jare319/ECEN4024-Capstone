using System.IO;
using System.IO.Pipes;

namespace OceanMotion;

public static class Program
{
    static void Main(String[] args) {
        string pipeName = "OceanMotion";
        
        using (NamedPipeServerStream pipeServer = new NamedPipeServerStream(pipeName, PipeDirection.InOut))
        {
            Console.WriteLine("Waiting for connection...");
            pipeServer.WaitForConnection();
            Console.WriteLine("Client connected.");

            using (StreamReader reader = new StreamReader(pipeServer))
            using (StreamWriter writer = new StreamWriter(pipeServer))
            {
                while (true)
                {
                    string command = reader.ReadLine();
                    Console.WriteLine("Received message from client: " + command);

                    string status = ProcessCommand(command);
                    // Echo the message back to the client
                    writer.WriteLine("Status: " + status);
                    writer.Flush(); // Flush the buffer to ensure the message is sent immediately
                }
            }
        }
    }

    private static string ProcessCommand(string command) {
        string[] args = command.Split(',');
        command = args[0];
        args = args.Skip(1).ToArray();
        switch (command)
        {
            case "Command1":
                
                return "Command1 received";
            case "ProcessInput":
                FileHandler fh = new FileHandler();
                ValidationParameters valParams = new ValidationParameters(100,10,10,10);
                int status = fh.ValidateFile(args[0],valParams);
                return "File processing returned status:" + status;
            case "Exit":

                return "Exit received, exiting...";
            // Insert additional commands as needed here.
            default:
                return "Unknown command received.";
        }
    }
}
