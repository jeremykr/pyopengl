from OpenGL.GL import *

# Returns shader IDs for created shaders.
def loadShader(filename, shader_type):
    # Read shader from file
    shader = []
    with open(filename, "rb") as f:
        shader = f.read()

    # Create & compile shaders
    sid = glCreateShader(shader_type)
    glShaderSource(sid, [shader])
    glCompileShader(sid)

    # Check compilation status
    result = glGetShaderiv(sid, GL_COMPILE_STATUS)
    log_length = glGetShaderiv(sid, GL_INFO_LOG_LENGTH)
    if log_length > 0:
        message = glGetShaderInfoLog(sid)
        print(message)
        return None

    return sid # Shader ID

# `shader_dict` is a dictionary with the GL shader type as a key
# and the filename as the value.
# Returns the shader program ID.
def makeProgram(shader_dict):
    pid = glCreateProgram()
    # Attach shaders
    for stype in shader_dict:
        sid = loadShader(shader_dict[stype], stype)
        shader_dict[stype] = sid
        glAttachShader(pid, sid)
    
    # Link program
    glLinkProgram(pid)

    # Check compilation status
    result = glGetProgramiv(pid, GL_LINK_STATUS)
    log_length = glGetProgramiv(pid, GL_INFO_LOG_LENGTH)
    if log_length > 0:
        message = glGetProgramInfoLog(pid)
        print(message)
        return None

    # Detach & delete shaders
    for stype in shader_dict:
        sid = shader_dict[stype]
        glDetachShader(pid, sid)
        glDeleteShader(sid)
    
    return pid