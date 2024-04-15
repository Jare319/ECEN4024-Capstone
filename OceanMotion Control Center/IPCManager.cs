using System.IO.Pipes;

namespace OceanMotion;

public class IPCManager
{

    private string pipeName = "OceanMotion";
    
    // Insert code for the event handler so the IPC manager can request data from Main when needed.

    public async Task RunAsnyc()
    {
        using (NamedPipeServerStream pipeServer = new NamedPipeServerStream(pipeName, PipeDirection.InOut))
        {
            Console.WriteLine("Waiting for connection...");
            await pipeServer.WaitForConnectionAsync();
            Console.WriteLine("Client connected.");

            using (StreamReader reader = new StreamReader(pipeServer))
            using (StreamWriter writer = new StreamWriter(pipeServer))
            {
                while (true)
                {
                    string command = await reader.ReadLineAsync();
                    Console.WriteLine("Received command from client: " + command);

                    // Process the command asynchronously
                    string response = await ProcessCommandAsync(command);

                    // Send the response back to the client
                    await writer.WriteLineAsync(response);
                    await writer.FlushAsync(); // Flush the buffer to ensure the message is sent immediately
                }
            }
        }
    }

    private async Task<string> ProcessCommandAsync(string command) {
        switch (command)
        {
            case "Command1":
                return await Task.FromResult("Command 1");
            case "Exit":

                return await Task.FromResult("Exiting...");
            // Insert additional commands as needed here.
            default:
                return await Task.FromResult("Invalid Option");
        }
    }
}