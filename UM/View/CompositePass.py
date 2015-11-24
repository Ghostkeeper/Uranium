# Copyright (c) 2015 Ultimaker B.V.
# Cura is released under the terms of the AGPLv3 or higher.

from UM.Resources import Resources

from UM.View.RenderPass import RenderPass
from UM.View.GL.OpenGL import OpenGL

class CompositePass(RenderPass):
    def __init__(self, name, width, height):
        super().__init__(name, width, height)

        self._shader = OpenGL.getInstance().createShaderProgram(Resources.getPath(Resources.Shaders, "composite.shader"))
        self._gl = OpenGL.getInstance().getBindingsObject()

    def setCompositeShader(self, shader):
        self._shader = shader

    def renderContents(self):
        pass

    def renderOutput(self):
        self._shader.bind()

        texture_unit = 0
        for render_pass in renderer.getRenderPasses():
            self._gl.glActiveTexture(texture_unit)
            self._gl.glBindTexture(self._gl.GL_TEXTURE_2D, render_pass.getTextureId())
            texture_unit += 1

        self._shader.setUniformValue("u_layer_count", texture_unit + 1)
        self._shader.setUniformValueArray("u_layers", [range(0, texture_unit)], texture_unit + 1)

        self.renderQuad()

        self._shader.release()
