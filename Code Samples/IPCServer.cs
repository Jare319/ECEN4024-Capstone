using System;
using System.IO.Pipes;
using System.Text;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
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
                    string message = reader.ReadLine();
                    Console.WriteLine("Received message from client: " + message);

                    // Echo the message back to the client
                    writer.WriteLine("Server received: " + message);
                    writer.Flush(); // Flush the buffer to ensure the message is sent immediately
                }
            }
        }
    }
}