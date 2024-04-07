using System.IO;
using System.IO.Pipes;

namespace OceanMotion;

public static class Program
{
    static void Main(String[] args) {
        IPCManager server = new IPCManager();
        server.RunAsnyc();
        // Subscribe to IPCManager event

        //FileHandler fh = new FileHandler();
        //Console.WriteLine(fh.ValidateFile(".\\testData1.txt", 10, 0, 2, 0.0001));
        bool ExitFlag = false;

        while (!ExitFlag) {

        }
    }
}
