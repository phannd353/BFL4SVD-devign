/* graph-for-funcs.scala

   This script returns a Json representation of the graph resulting in combining the
   AST, CGF, and PDG for each method contained in the currently loaded CPG.

   Input: A valid CPG
   Output: Json

   Running the Script
   ------------------
   see: README.md

   The JSON generated has the following keys:

   "functions": Array of all methods contained in the currently loaded CPG
     |_ "function": Method name as String
     |_ "id": Method id as String (String representation of the underlying Method node)
     |_ "AST": see ast-for-funcs script
     |_ "CFG": see cfg-for-funcs script
     |_ "PDG": see pdg-for-funcs script
 */

import scala.jdk.CollectionConverters._


import io.shiftleft.codepropertygraph.generated.EdgeTypes
import io.shiftleft.codepropertygraph.generated.NodeTypes
import io.shiftleft.codepropertygraph.generated.nodes
import io.shiftleft.semanticcpg.language._

import overflowdb._

private def quote(value: String): String =
  "\"" + value.flatMap {
    case '\\' => "\\\\"
    case '"'  => "\\\""
    case '\n' => "\\n"
    case '\r' => "\\r"
    case '\t' => "\\t"
    case c if c < ' ' => f"\\u${c.toInt}%04x"
    case c => c.toString
  } + "\""

private def nodeJson(node: nodes.AstNode): String = {
  val edges = (node.inE("AST").l ++ node.inE("CFG").l ++ node.outE("AST").l ++ node.outE("CFG").l).map { edge =>
    s"""{"id":${quote(edge.toString)},"in":${quote(edge.src.toString)},"out":${quote(edge.dst.toString)}}"""
  }.mkString("[", ",", "]")
  val properties = node.propertiesMap.asScala.map { case (key, value) =>
    s"""{"key":${quote(key)},"value":${quote(value.toString)}}"""
  }.mkString("[", ",", "]")
  s"""{"id":${quote(node.toString)},"edges":$edges,"properties":$properties}"""
}

@main def main(inputPath: String, outputPath: String): Unit = {
  importCpg(inputPath)
  val functions =
    cpg.method.map { method =>
      val methodName = method.fullName
      val methodId = method.toString
      val methodFile = method.location.filename
      val astChildren = method.astMinusRoot.l
      val ast = astChildren.map(nodeJson).mkString("[", ",", "]")
      val cfg = "[]"
      val pdg = "[]"
      s"""{"function":${quote(methodName)},"file":${quote(methodFile)},"id":${quote(methodId)},"AST":$ast,"CFG":$cfg,"PDG":$pdg}"""
    }.l.mkString("[", ",", "]")
  java.nio.file.Files.writeString(
    java.nio.file.Paths.get(outputPath),
    s"""{"functions":$functions}"""
  )
}
