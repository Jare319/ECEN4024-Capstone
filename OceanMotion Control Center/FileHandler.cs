using System.IO;

namespace OceanMotion;

public class FileHandler {
    
    private StreamReader? sr;
    //private StreamWriter sw; for writing to create


    public int ValidateFile(String path, ValidationParameters valParams) {
        return ReadFile(path, valParams);
    }

    private int ReadFile(String path, ValidationParameters valParams) {
        String? line1;
        String? line2;
        int stopCode = 1;
        try {
            // REFACTOR***
            sr = new StreamReader(path);
            line1 = sr.ReadLine();
            line2 = sr.ReadLine();
            double time;
            if (line1.Split(',').Length is not (7 or 2)) { // Catches if the file isn't in the proper format. Either 7 (time + 6-dof) or 2 (time + heave) columns.
                // Return err# for improper data file format
                Console.WriteLine("Improper data format");
                return -3;
            } else if (!double.TryParse(line1.Split()[0],out time) && double.TryParse(line2.Split()[0],out time)) { // Catches if the file has headers and corrects for it.
                line1 = line2; // Increments line1 without further parsing. Line2 will be incremented automatically by the loop.
                line2 = sr.ReadLine();
                Console.WriteLine("You shouldn't be here");
            }
            
            while (line2 != null && stopCode == 1) {
                stopCode = Validate(line1.Split(','), line2.Split(','), valParams); // Will read file lines until completion, or a line occurs that defies the maximums set.
                line1 = line2;
                line2 = sr.ReadLine();
            }
            sr.Close();
        }
        catch(FileNotFoundException e) {
            // Log & display error
            Console.WriteLine(e.Message);
            return -1;
        }
        catch(IOException e) { // Triggered when file is empty I believe
            // Log & display error
            Console.WriteLine(e.Message);
            return -2;
        }
        catch(Exception e) {
            //catch other errors
            Console.WriteLine(e.Message);
            return -3;
        }
        return stopCode;
    }
    private int Validate(String[] line1, String[] line2, ValidationParameters valParams) {
        double period;
        double vel;
        //int fileType; // Will want to include some info on which type of file this is: 1 dof or 6 dof.
        try {
            period = double.Parse(line2[0])-double.Parse(line1[0]);
            vel = System.Math.Abs((double.Parse(line2[1])-double.Parse(line1[1]))/period);
            if (period < valParams.getMinTimeStep()) {
                Console.WriteLine("Timestep too small");
                return -4; // Timestep is too small.
            }
            if (vel > valParams.getMaxVelocity()) {
                Console.WriteLine("Velocity too high");
                return -5;
            }
            if (double.Parse(line1[1]) > valParams.getMaxHeight() || double.Parse(line2[1]) > valParams.getMaxHeight()) {
                Console.WriteLine("Max displacement exceeded.");
                return -6;
            }
            if (double.Parse(line1[1]) < valParams.getMinHeight() || double.Parse(line2[1]) < valParams.getMinHeight()) {
                Console.WriteLine("Min displacement exceeded.");
                return -7;
            }
            
        } catch(Exception e) {
            Console.WriteLine(e.Message);
            return -3; // improper data format err# here
        }
        return 1;
    }
}